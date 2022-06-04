;; this is an example of simple Qt5 app written in ChiakiLisp
;; to run this example in the AST mode (default):
;; $ ./chiakilang examples/eval-mode/qt5-simple-app.window.cl

;; let's import all required modules in order to work with Qt
(import PyQt5.QtWidgets)
(import PyQt5.QtGui)
(import PyQt5.QtCore)

;; since we don't allow module/class/attr syntax (maybe yet),
;; we need to store module/class at the global variable 'Qt'.
(def Qt QtCore/Qt)

;; you do not need to define (defn main (argc argv)) function
;; although, in the AST mode, you can refer to argc, and argv
;; *implicitly defined* variables passed to the script

;; the last expression result of (let) block will be returned
(let (application (QtWidgets/QApplication argv)
      window      (QtWidgets/QWidget)
      layout      (QtWidgets/QVBoxLayout window)
      title       (QtWidgets/QLabel "ChiakiLisp")
      pixmap      (QtGui/QPixmap "./CL.png")
      picture     (QtWidgets/QLabel)
      copyright   (QtWidgets/QLabel "@jedi2light May, 2022"))
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