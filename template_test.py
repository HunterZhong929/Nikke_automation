import template
import PIL.Image
import numpy as np

def main():
    template_name = "defense_post_button.png"
    #template.load(template_name)
    template.try_load("not exist name")
    template.try_load(template_name)
    template._LOADED_TEMPLATES[template_name].show()



    test_specifcation = template.Specification("defense_post_button.png")
    client_pos = test_specifcation.load_pos()
    client_pos.show()
    if client_pos:
        cv_pos = np.array(client_pos.convert("L"))
    x,y= np.where(cv_pos == 255)
    
    pos = (x[5],y[5])
    print(pos)
    game_image = PIL.Image.open("last_screenshot.png")
    test_specifcation.match(game_image,pos)
    

    iter = template.match(game_image, "defense_post_button.png","get_defense_reward.png","matome_destroy.png")
    next(iter)
    next(iter)
    #next(iter)
if __name__ == "__main__":
    main()

