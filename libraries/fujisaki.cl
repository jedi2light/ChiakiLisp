;; Fujisaki is a small declarative (PyQt5 based) UI toolkit

(import sys)

(import PyQt5.QtGui)
(import PyQt5.QtCore)
(import PyQt5.QtWidgets)

(def    Qt    QtCore/Qt)

(defn vbox ()
 (let (qt-app             (QtWidgets/QApplication sys/argv)
       window             (QtWidgets/QWidget))
  {:window window
   :qt-app qt-app :layout (QtWidgets/QVBoxLayout window)}))

(defn label (layout text & props)
 (let (qt-layout          (:layout          layout)
       alignment          (:alignment props :center)
       qt-label-instance  (QtWidgets/QLabel))
  (.setText qt-label-instance text)
  (when (= alignment :center)
   (.setAlignment qt-label-instance Qt/AlignCenter))
  (.addWidget qt-layout qt-label-instance)
  layout))

(defn image (layout image-path & props)
 (let (qt-layout          (:layout          layout)
       alignment          (:alignment props :center)
       qt-label-instance  (QtWidgets/QLabel))
  (.setPixmap qt-label-instance (QtGui/QPixmap image-path))
  (when (= alignment :center)
   (.setAlignment qt-label-instance Qt/AlignCenter))
  (.addWidget qt-layout qt-label-instance)
  layout))

(defn window (layout config & props)
 (let (width       (:width  config 350)
       height      (:height config 150)
       title       (:title  config "FujisakiUI App Window")
       window      (:window layout)
       application (:qt-app layout))
  (.resize         window   width  height)
  (.setWindowTitle window   title)
  (.show           window)
  (.exec           application)))
