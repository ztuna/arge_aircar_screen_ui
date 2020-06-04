import QtQuick 2.4
import SDK 1.0
import QtQuick.Layouts 1.1


Rectangle {
    id: root
    Layout.alignment: Layout.Center
    width: 160
    height: 145
    color: "#181818"
    property string suffix: "A"
    property int minVal: 0
    property int maxVal: 100
    property real actVal: 100

    Connections{
        target: batteryWidget
        onCurrentValueChanged: root.actVal = batteryWidget.currentValue
    }

    Rectangle {
        Layout.alignment: Layout.Center
        width: 160
        height: 145
        color: "#1d1d35"
        border.color: "#000000"
        border.width: 3
        Text {
            id: name
            text: "Battery Current"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 5
            font.pointSize: 13
            color: "#6affcd"
        }

        RadialBar {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            width: parent.width / 1.4
            height: width - (0.001)*actVal
            penStyle: Qt.RoundCap
            progressColor: "#6affcd"
            foregroundColor: "#191a2f"
            dialWidth: 11
            minValue: minVal
            maxValue: maxVal
            value: actVal
            suffixText: suffix
            textFont {
                family: "Halvetica"
                italic: false
                pointSize: 18
            }
            textColor: "#00ffc1"
        }
    }
}
