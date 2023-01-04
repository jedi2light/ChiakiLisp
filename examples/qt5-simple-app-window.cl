;; Qt5 Simple App Window example
;; Run with: ./chiakilang ./examples/qt5-simple-app-window.cl

;; Here we're using `import` form to import needed Qt modules
(import PyQt5.QtWidgets)
(import PyQt5.QtGui)
(import PyQt5.QtCore)

;; Here is the little hack because of lacking `a/b/c` syntax.
(def Qt QtCore/Qt)

;; Here we're using `let` to declare bindings and run the app
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