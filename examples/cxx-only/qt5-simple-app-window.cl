;; this is an example of simple Qt5 app written in ChiakiLisp
;; to compile & run this example run the following:
;; $ ./chiakilangc examples/cxx-only/qt5-simple-app.window.cl

;; tell ./chiakilangc to add this directory to lookup headers
(hpp-base-dir "/usr/include/qt")

;; tell ./chiakilangc to link generated binary with a library
(link Qt5Core)
(link Qt5Gui)
(link Qt5Widgets)

;; translates into '#include <some/path/to/header>' statement
(include QtWidgets/QApplication)
(include QtWidgets/QWidget)
(include QtWidgets/QVBoxLayout)
(include QtWidgets/QLabel)

;; you do not need to define (defn main (argc argv)) function
;; although, in compiler mode, you can refer to argc and argv
;; *implicitly defined* variables passed to the main() 

;; you should use (new (Class arg1 arg2 ...)) form to express
;; dynamic allocation; thus LHS variables becomes C++ pointer

;; ChiakiLisp C++ code generator'll automagically resolve the
;; way object member access should be expressed in a C++ code
;; so you do not need to write '->' instead of '.' explicilty

;; the last expression result of (let) block will be returned
(let (application (QApplication argc argv)
      window      (new (QWidget))
      layout      (new (QVBoxLayout window))
      title       (new (QLabel "ChiakiLisp"))
      pixmap      (QPixmap "./CL.png")
      picture     (new (QLabel))
      copyright   (new (QLabel "@jedi2light May, 2022")))
 (.setAlignment title Qt/AlignCenter)
 (.setPixmap picture pixmap)
 (.setAlignment picture Qt/AlignCenter)
 (.setAlignment copyright Qt/AlignCenter)
 (.addWidget layout title)
 (.addWidget layout picture)
 (.addWidget layout copyright)
 (.resize window 350 150)
 (.setWindowTitle window "ChiakiLisp @jedi2light 2022 WTFPL")
 (.show window)
 (.exec application))