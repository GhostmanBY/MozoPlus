resumen_estilo_scroll = f"""
            QScrollArea {{
                border: 2px solid #DEB887;
                border-radius: 10px;
                background-color: #FEFCF8;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #FDF5E6;
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #8B4513;
                min-height: 30px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

Header_Frame_Style = """
    QFrame {
        background-color: #FFF8DC;
        border-radius: 10px;
        padding: 5px;
    }
"""

# Variable: title_label
Title_Label_Style = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #8B4513;
        padding: 5px;
        border-bottom: 2px solid #DEB887;
    }
"""

# Variable: fecha_label y mozo_label
Icon_Label_Style = "font-size: 16px;"

# Variable: fecha_input y mozo_input
Search_Input_Style = """
    QLineEdit {
        padding: 8px;
        border: 2px solid #DEB887;
        border-radius: 5px;
        background: white;
        font-size: 14px;
        min-width: 200px;
    }
    QLineEdit:focus {
        border-color: #8B4513;
    }
"""

# Variable: search_button
Search_Button_Style = """
    QPushButton {
        background-color: #8B4513;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        min-width: 100px;
    }
    QPushButton:hover {
        background-color: #A0522D;
    }
    QPushButton:pressed {
        background-color: #6B4423;
    }
"""

# Variable: load_button
Load_Button_Style = """
    QPushButton {
        background-color: #CD853F;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        min-width: 100px;
    }
    QPushButton:hover {
        background-color: #8B4513;
    }
    QPushButton:pressed {
        background-color: #6B4423;
    }
"""

# Variable: scroll_area
Info_Scroll_Area_Style = """
    QScrollArea {
        border: 2px solid #DEB887;
        border-radius: 10px;
        background-color: #FEFCF8;
        min-height: 850px;
    }
    QScrollBar:vertical {
        border: none;
        background: #FDF5E6;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #8B4513;
        min-height: 30px;
        border-radius: 6px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

# MARK: load_summary
# Variable: fecha_frame
Summary_Fecha_Frame_Style = """
    QFrame {
        background-color: #FFF8DC;
        border-radius: 15px;
        margin: 10px;
        padding: 15px;
    }
"""

# Variable: fecha_label
Summary_Fecha_Label_Style = """
    QLabel {
        font-size: 18px;
        font-weight: bold;
        color: #8B4513;
        padding: 5px;
        border-bottom: 2px solid #DEB887;
    }
"""

# Variable: entry_frame
Summary_Entry_Frame_Style = """
    QFrame {
        background-color: white;
        border: 1px solid #DEB887;
        border-radius: 10px;
        margin: 5px;
        padding: 15px;
    }
    QFrame:hover {
        border: 1px solid #8B4513;
        background-color: #FEFCF8;
    }
"""

# Variable: info_label
Summary_Info_Label_Style = """
    QLabel {
        font-size: 14px;
        color: #6B4423;
        margin: 3px 0;
    }
"""

# Variable: productos_detalle
Summary_Productos_Detalle_Style = """
    QLabel {
        color: #6B4423;
        margin-left: 15px;
        font-size: 13px;
    }
"""

Detail_Total_Style = """
    font-size: 18px;
    font-weight: bold;
    color: #2E7D32;
    margin-top: 10px;
    padding: 10px;
    background-color: #E8F5E9;
    border: 2px solid #1A561D;
    border-radius: 5px;
"""