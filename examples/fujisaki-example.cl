(require libraries/fujisaki)

(-> (fujisaki/vbox)
    (fujisaki/label  "ChiakiLisp"
                     {:alignment :center})
    (fujisaki/image  "./Logo.png"
                     {:alignment :center})
    (fujisaki/label  "ChiakiLisp @jedi2light May, 2023"
                     {:alignment :center})
    (fujisaki/window {:width  350
                      :height 150 
                      :title  "ChiakiLisp @jedi2light May, 2023 WTFPL"}))
