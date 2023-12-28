import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout, QDialog, QInputDialog
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter, ImageEnhance
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

image_saved_name = ''

workdir = ''
changes_not_saved = False
selected_name = ''

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(900, 500)

layout_main = QHBoxLayout()
btn_directory = QPushButton('Папка')
list_files = QListWidget()
picture = QLabel()
edit_placeholder = QLabel('Нажмите "Папка" и выберите папку с изображениями которые вы хотите отредактировать, затем выберите из списка\nизображение которое вы хотите отредактировать.')
edit_placeholder2 = QLabel('Изображение сохранено как '+image_saved_name)
edit_placeholder2.hide()

list_files.setMaximumWidth(250)
main_win.setMaximumHeight(500)
main_win.setMaximumWidth(900)
main_win.setMinimumHeight(500)
main_win.setMinimumWidth(900)

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало ↔')
btn_mirror_ud = QPushButton('Зеркало ↕')
btn_enhance = QPushButton('Насыщенность')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Размытие')
btn_save = QPushButton('Сохранить изменения в новом файле')

btn_contur = QPushButton('Только края')
btn_find_edges = QPushButton('Неон')
btn_sharpen = QPushButton('Резкость')

edit_buttons = [btn_left, btn_right, btn_mirror, btn_mirror_ud, btn_enhance, btn_bw, btn_blur, btn_contur, btn_find_edges, btn_sharpen]
for i in edit_buttons:
    i.hide()

vbox1 = QVBoxLayout()
vbox2 = QVBoxLayout()
hbox1 = QHBoxLayout()
hbox2 = QHBoxLayout()

vbox1.addWidget(btn_directory)
vbox1.addWidget(list_files)
vbox2.addWidget(picture)
hbox1.addWidget(btn_left)
hbox1.addWidget(btn_right)
hbox1.addWidget(btn_mirror)
hbox1.addWidget(btn_mirror_ud)
hbox1.addWidget(btn_enhance)
hbox2.addWidget(btn_bw)
hbox2.addWidget(btn_blur)
hbox2.addWidget(btn_contur)
hbox2.addWidget(btn_find_edges)
hbox2.addWidget(btn_sharpen)
vbox2.addWidget(btn_save)
layout_main.addLayout(vbox1)
layout_main.addLayout(vbox2)
vbox2.addLayout(hbox1)
vbox2.addLayout(hbox2)
vbox2.addWidget(edit_placeholder, alignment=Qt.AlignBottom)
vbox2.addWidget(edit_placeholder2, alignment=Qt.AlignBottom)
btn_save.hide()

def folder_chose():
    global workdir
    try:
        list_files.clear()
        picture.clear()
        for o in edit_buttons:
            o.hide()
        edit_placeholder.show()
        btn_save.hide()
        workdir = QFileDialog.getExistingDirectory()
        filenames = os.listdir(workdir)
        supported = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
        for i in filenames:
            for j in supported:
                if i.endswith(j):
                    list_files.addItem(i)
    except:
        pass

def reloadlist():
    global workdir
    filenames = os.listdir(workdir)
    supported = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    list_files.clear()
    for i in filenames:
        for j in supported:
            if i.endswith(j):
                list_files.addItem(i)

def show_image():
    global selected_name
    global changes_not_saved
    changes_not_saved = False
    edit_placeholder.hide()
    edit_placeholder2.hide()
    for i in edit_buttons:
        i.show()
    btn_save.hide()
    selected_name = list_files.selectedItems()[0].text()
    with Image.open(workdir+'/'+selected_name) as image:
        image.save('currect_edit.png')
    pixmap = QPixmap(workdir+'/'+selected_name)
    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
    picture.setPixmap(pixmap)
    
def save():
    global workdir
    global selected_name
    global changes_not_saved
    global image
    global image_saved_name
    changes_not_saved = False
    btn_save.hide()
    with open('modify_counts.txt', 'r', encoding='utf-8') as file:
        counts = file.read()
        counts = int(counts)
        counts += 1
        if selected_name.endswith('.jpeg'):
            selection = -5
        else:
            selection = -4
        image.save(workdir+'/'+selected_name[0:len(selected_name)+selection]+'_'+str(counts)+'.png')
        reloadlist()
        for i in edit_buttons:
            i.hide()
        image_saved_name = selected_name[0:len(selected_name)+selection]+'_'+str(counts)+'.png'
        edit_placeholder2.setText('Изображение сохранено как '+image_saved_name)
        edit_placeholder2.show()
        with open('modify_counts.txt', 'w', encoding='utf-8') as file2:
            file2.write(str(counts))

def ask(Window_title, question):
    deal = QDialog()
    b1 = QPushButton('Ок', deal)
    b2 = QPushButton('Отмена', deal)
    asking = QLabel(question)
    main_deal = QVBoxLayout()
    dealh1 = QHBoxLayout()
    dealh2 = QHBoxLayout()
    deal.setLayout(main_deal)
    main_deal.addLayout(dealh1)
    main_deal.addLayout(dealh2)
    dealh1.addWidget(asking)
    dealh2.addWidget(b1)
    dealh2.addWidget(b2)
    deal.setWindowTitle(Window_title)
    deal.setWindowModality(Qt.ApplicationModal)
    b1.clicked.connect(deal.accept)
    b2.clicked.connect(deal.reject)
    result = deal.exec_()
    if result == QDialog.Accepted:
        return True
    else:
        return False
'''
def hide_edit():
    btn_left.hide()
    btn_right.hide()
    btn_mirror.hide()
    btn_sharpness.hide()
    btn_bw.hide()
    btn_blur.hide()

def show_edit():
    btn_left.show()
    btn_right.show()
    btn_mirror.show()
    btn_sharpness.show()
    btn_bw.show()
    btn_blur.show()
'''
def lefting():
    try:
        global image
        global workdir
        global changes_not_saved
        btn_save.show()
        if changes_not_saved == False:
            changes_not_saved = True
            selected_name = list_files.selectedItems()[0].text()
            with Image.open(workdir+'/'+selected_name) as image:
                image = image.transpose(Image.ROTATE_90)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            image = image.transpose(Image.ROTATE_90)
            image.save('currect_edit.png')
            pixmap = QPixmap('currect_edit.png')
            pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
            picture.setPixmap(pixmap)
    except:
        pass

def righting():
    try:
        global image
        global workdir
        global changes_not_saved
        btn_save.show()
        if changes_not_saved == False:
            changes_not_saved = True
            selected_name = list_files.selectedItems()[0].text()
            with Image.open(workdir+'/'+selected_name) as image:
                image = image.transpose(Image.ROTATE_270)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            image = image.transpose(Image.ROTATE_270)
            image.save('currect_edit.png')
            pixmap = QPixmap('currect_edit.png')
            pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
            picture.setPixmap(pixmap)
    except:
        pass

def mirror():
    try:
        global image
        global workdir
        global changes_not_saved
        btn_save.show()
        if changes_not_saved == False:
            changes_not_saved = True
            selected_name = list_files.selectedItems()[0].text()
            with Image.open(workdir+'/'+selected_name) as image:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.save('currect_edit.png')
            pixmap = QPixmap('currect_edit.png')
            pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
            picture.setPixmap(pixmap)
    except:
        pass

def mirror_ud():
    try:
        global image
        global workdir
        global changes_not_saved
        btn_save.show()
        if changes_not_saved == False:
            changes_not_saved = True
            selected_name = list_files.selectedItems()[0].text()
            with Image.open(workdir+'/'+selected_name) as image:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                image = image.transpose(Image.ROTATE_180)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image = image.transpose(Image.ROTATE_180)
            image.save('currect_edit.png')
            pixmap = QPixmap('currect_edit.png')
            pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
            picture.setPixmap(pixmap)
    except:
        pass

def bw():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что хотите наложить\nчёрно-белый фильтр? если\nвы это сделаете вы не сможете это\nотменить!')
        if is_ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = image.convert('L')
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = image.convert('L')
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

def enhacing():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что изменить резкость\nизображения? если вы это\nсделаете вы не сможете это\nотменить!')
        if is_ok:
            level, ok = QInputDialog.getText(main_win, 'Резкость', 'Введите множитель насыщенности:')
        if is_ok and ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = ImageEnhance.Contrast(image)
                    image = image.enhance(float(level))
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = ImageEnhance.Contrast(image)
                image = image.enhance(float(level))
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

def bluring():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что хотите наложить\nразмытый фильтр? если\nвы это сделаете вы не сможете это\nотменить!')
        if is_ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = image.filter(ImageFilter.BLUR)
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = image.filter(ImageFilter.BLUR)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

def contur():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что хотите наложить\nфильтр оставляющий только края? если\nвы это сделаете вы не сможете это\nотменить!')
        if is_ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = image.filter(ImageFilter.CONTOUR)
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = image.filter(ImageFilter.CONTOUR)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

def find_edges():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что хотите наложить\nфильтр неона? если\nвы это сделаете вы не сможете это\nотменить!')
        if is_ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = image.filter(ImageFilter.FIND_EDGES)
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = image.filter(ImageFilter.FIND_EDGES)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

def sharpness():
    try:
        global image
        global workdir
        global changes_not_saved
        is_ok = ask('Подтверждение действия', 'Вы уверены что хотите наложить\nразмытый фильтр? если\nвы это сделаете вы не сможете это\nотменить!')
        if is_ok:
            btn_save.show()
            if changes_not_saved == False:
                changes_not_saved = True
                selected_name = list_files.selectedItems()[0].text()
                with Image.open(workdir+'/'+selected_name) as image:
                    image = image.filter(ImageFilter.SHARPEN)
                    image.save('currect_edit.png')
                    pixmap = QPixmap('currect_edit.png')
                    pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                    picture.setPixmap(pixmap)
            else:
                image = image.filter(ImageFilter.SHARPEN)
                image.save('currect_edit.png')
                pixmap = QPixmap('currect_edit.png')
                pixmap = pixmap.scaled(picture.width(), picture.height(), Qt.KeepAspectRatio)
                picture.setPixmap(pixmap)
        else:
            pass
    except:
        pass

btn_directory.clicked.connect(folder_chose)
list_files.itemClicked.connect(show_image)
btn_save.clicked.connect(save)
btn_left.clicked.connect(lefting)
btn_right.clicked.connect(righting)
btn_mirror.clicked.connect(mirror)
btn_mirror_ud.clicked.connect(mirror_ud)
btn_enhance.clicked.connect(enhacing)
btn_blur.clicked.connect(bluring)
btn_contur.clicked.connect(contur)
btn_find_edges.clicked.connect(find_edges)
btn_sharpen.clicked.connect(sharpness)

btn_bw.clicked.connect(bw)

main_win.setLayout(layout_main)
main_win.show()
app.exec_()