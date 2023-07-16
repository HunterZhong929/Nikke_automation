# -*- coding=UTF-8 -*-
# pyright: strict

import time
from typing import Callable, Iterable, Iterator, Text, Tuple, TypeVar, Union
import device
import template
import config
import mathtools

default_device = device.Device(config.config.WINDOW_HANDLE)
TARGET_WIDTH = 1080 #temporary name for now, later this should be refactored
def resize_proxy() -> mathtools.ResizeProxy:
    """Resize proxy to current client width."""
    print("debug4")
    #default_device = device.Device(config.config.WINDOW_HANDLE)
    return mathtools.ResizeProxy(default_device.width())


def count_image(*tmpl: Union[Text, template.Specification]) -> int:
    ret = 0
    for _ in template.match(default_device.screenshot(), *tmpl):
        ret += 1
    return ret


def match_image_until_disappear(
    *tmpl: Union[Text, template.Specification],
    sort: Callable[
        [Iterator[Tuple[template.Specification, Tuple[int, int]]]],
        Iterable[Tuple[template.Specification, Tuple[int, int]]],
    ] = lambda x: x,
) -> Iterator[Tuple[template.Specification, Tuple[int, int]]]:
    while True:
        count = 0
        for i in sort(template.match(default_device.screenshot(max_age=0), *tmpl)):
            count += 1
            yield i
            break  # actions will make screenshot outdate
        if count == 0:
            break


def wait_image(
    *tmpl: Union[Text, template.Specification],
    timeout: float = float("inf"),
) -> Tuple[template.Specification, Tuple[int, int]]:
    deadline = time.time() + timeout
    while True:
        try:
            #match the screenshot with all the inputted templates, note that this match is a generator
            return next(template.match(default_device.screenshot(max_age=0), *tmpl))
        except StopIteration:
            if time.time() > deadline:
                raise TimeoutError()
            time.sleep(0.01)


def wait_image_stable(
    *tmpl: Union[Text, template.Specification],
    duration: float = 1.0,
    timeout: float = float("inf"),
) -> Tuple[template.Specification, Tuple[int, int]]:
    deadline = time.time() + timeout
    t, last_pos = wait_image(*tmpl, timeout=timeout)
    last_changed_time = time.time()
    while True:
        time.sleep(0.01)
        _, pos = wait_image(t, timeout=deadline - time.time())
        if pos != last_pos:
            last_changed_time = time.time()
        if time.time() - last_changed_time > duration:
            break
        if time.time() > deadline:
            raise TimeoutError()
        last_pos = pos
    return t, last_pos


T = TypeVar("T")


def run_with_retry(fn: Callable[[], T], max_retry: int = 10, delay: float = 1) -> T:
    try:
        return fn()
    except Exception:
        if max_retry <= 0:
            raise
        time.sleep(delay)
        return run_with_retry(fn, max_retry - 1, delay)


def wait_image_disappear(*tmpl: Union[Text, template.Specification]) -> None:
    while True:
        try:
            next(template.match(default_device.screenshot(max_age=0), *tmpl))
            time.sleep(0.5)
        except StopIteration:
            break


def template_rect(tmpl: template.Input, pos: Tuple[int, int]) -> device.Rect:
    print("debug3")
    rp = resize_proxy()
    print(rp)
    print(type(rp))
    img = template.load(template.Specification.from_input(tmpl).name)
    #return(100,200,300,400)
    return (*pos, *rp.vector2((img.width, img.height),TARGET_WIDTH))

    
def tap_image(
    tmpl: Union[Text, template.Specification], *, x: int = 0, y: int = 0
) -> bool:
    try:
        tmpl, pos = next(template.match(default_device.screenshot(), tmpl))
        img = template.load(tmpl.name)
        w, h = resize_proxy().vector2((img.width, img.height), TARGET_WIDTH)
        default_device.tap((pos[0] + x, pos[1] + y, w - x, h - y))
        return True
    except StopIteration:
        return False


def wait_tap_image(
    name: Union[Text, template.Specification], *, x: int = 0, y: int = 0
) -> None:
    tmpl, last_pos = wait_image(name)
    while True:
        tmpl, pos = wait_image(name)
        if pos == last_pos:
            break
        last_pos = pos
    img = template.load(tmpl.name)
    w, h = resize_proxy().vector2((img.width, img.height), TARGET_WIDTH)
    default_device.tap((pos[0] + x, pos[1] + y, w - x, h - y))


