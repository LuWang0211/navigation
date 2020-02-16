import QtQuick 2.2
import QtQuick.Window 2.2

Window {
    Image {
        id: background
        source: "temp1-1.png"
    }
    Image {
        id: arrow
        anchors.centerIn: parent
        source: "Capture.PNG"
        Behavior on rotation {
            NumberAnimation {
                duration: 250
            }
        }
    }
    MouseArea {
        anchors.fill: parent
        onPressed: {
            arrow.rotation -= 90
        }
    }
    visible: true
    width: background.width
    height: background.height
}