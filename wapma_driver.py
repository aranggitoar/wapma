import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


# Functions for entering keys and clicking objects in DOM
def enter_keys(string_to_find, find_by_what, keys_to_enter, driver):
    if find_by_what == 'css':
        e = driver.find_element_by_css_selector(string_to_find)
    elif find_by_what == 'xpath':
        e = driver.find_element_by_xpath(string_to_find)
    elif find_by_what == 'class':
        e = driver.find_element_by_class_name(string_to_find)
    e.send_keys(keys_to_enter)


def click(string_to_find, find_by_what, driver):
    if find_by_what == 'css':
        e = driver.find_element_by_css_selector(string_to_find)
    elif find_by_what == 'xpath':
        e = driver.find_element_by_xpath(string_to_find)
    elif find_by_what == 'class':
        e = driver.find_element_by_class_name(string_to_find)
    e.click()


# Function for selecting language from user input to navigate the DOM
def language_hook_conf(user_language, which_hook):
    if user_language == "Indonesian":
        if which_hook == 1:
            return "Cari atau"
        elif which_hook == 2:
            return "lebih"
        elif which_hook == 3:
            return "Anda"
        elif which_hook == 4:
            return "Ketik sebuah pesan"

    elif user_language == "Portuguese":
        if which_hook == 1:
            return "Pesquisar ou"
        elif which_hook == 2:
            return "mais"
        elif which_hook == 3:
            return "Você"
        elif which_hook == 4:
            return "Digite uma mensagem"

    elif user_language == "English":
        if which_hook == 1:
            return "Search or"
        elif which_hook == 2:
            return "more"
        elif which_hook == 3:
            return "You"
        elif which_hook == 4:
            return "Type a message"


def automation_main(**user_input):
    # Memeriksa apakah semua parameter sudah siap
    if not user_input["user_language"]:
        print("Anda belum mengatur bahasa!")
        raise SystemExit
    elif not user_input["group_name"]:
        print("Anda belum menentukan nama grup!")
        raise SystemExit
    elif not user_input["message_to_send"]:
        print("Anda belum menulis pesan yang akan dikirim!")
        raise SystemExit

    print('Otomasi dimulai..\n')

    # Membuka whatsapp lewat browser
    opt = Options()
    driver = webdriver.Chrome(options=opt, executable_path="./chromedriver")
    driver.get("https://web.whatsapp.com")

    # Tunggu sampai layar WA siap diakses
    time.sleep(10)
    status = 0
    while status == 0:
        try:
            driver.find_element_by_css_selector(
                'span[data-testid="default-user"]')
            status = 1
        except NoSuchElementException:
            time.sleep(10)
            print("Sabar, WA Anda belum terbuka..")
        if status == 1:
            time.sleep(7)
            break

    # Cari grup yang diinginkan
    status = 0
    while status == 0:
        try:
            click(
                '//div[contains(text(), "' +
                language_hook_conf(user_input["user_language"], 1) +
                '")]/following-sibling::label/div', 'xpath', driver)
            enter_keys(
                '//div[contains(text(), "' +
                language_hook_conf(user_input["user_language"], 1) +
                '")]/following-sibling::label/div/div[@contenteditable="true"]',
                'xpath', user_input["group_name"], driver)
            driver.find_element_by_xpath('//div[text()="' +
                                         user_input["group_name"] + '"]')
            status = 1
        except NoSuchElementException:
            time.sleep(2)
            print("Pencarian belum dilakukan..")
            status = 1
        if status == 1:
            break

    # Masuk dalam grup yang diinginkan
    status = 0
    while status == 0:
        try:
            click('//span[@title="' + user_input["group_name"] + '"]', 'xpath',
                  driver)
            driver.find_element_by_xpath('//span[@title="' +
                                         user_input["group_name"] + '"]')
            status = 1
        except NoSuchElementException:
            time.sleep(2)
            print("Masih mencari..")
            status = 1
        if status == 1:
            break

    # Buka menu informasi lebih dari grup
    click('//div[@id="main"]//span[text()="' + user_input["group_name"] + '"]',
          'xpath', driver)

    # Kalau ada banyak anggota buka opsi untuk tampilkan semua anggota
    status = 0
    while status == 0:
        try:
            click(
                '//div[contains(text(), "' +
                language_hook_conf(user_input["user_language"], 2) + '")]',
                'xpath', driver)
        except NoSuchElementException:
            status = 1
        if status == 1:
            break

    # 19 JULI SAMPAI SINI SUDAH OK

    # Metode di bawah tidak bisa dilakukan. Tiap anggota grup perlu
    # dipilih secara manual sambil melakukan scroll kepada elemen yang
    # mengandung data sebuah grup. Kurang lebih seperti ini caranya:
    # driver.execute_script("document.querySelector('div._3Bc7H.KPJpj').scroll(0, 5000)")

    # Harus dipilih secara manual karena data setiap anggota grup tidak
    # langsung muncul dalam elemen div._3Bc7H.KPJpj, melainkan diperbarui
    # oleh kode Elixir di backend setiap scroll dilakukan pada elemen
    # tersebut. Pemilihan secara manual ini dapat dilakukan dengan
    # mengukur properti transform: translateY() yang berubah setiap scroll
    # dilakukan, relatif terhadap properti height elemen div._3uIPm.WYyr1.

    # Gunakan akun pribadi untuk dapatkan atribut kelas dari sel-sel anggota grup
    group_participant_cell_class_name_hook = '//span[@title="' + language_hook_conf(
        user_input["user_language"], 3) + '" ]/../../../..'
    group_participant_cell_class_name_driver = driver.find_element_by_xpath(
        group_participant_cell_class_name_hook)
    print(group_participant_cell_class_name_driver)
    group_participant_cell_class_name = group_participant_cell_class_name_driver.get_attribute(
        'class')
    # Dua baris dibawah ini contoh saja, baris pertama dari grup kode di
    # bawah tidak berfungsi karena atribut kelas yang didapatkan itu dua
    # dan terpisah oleh sebuah spasi.
    group_participant_cell_class_name = group_participant_cell_class_name.split(
    )
    group_participant_cell_class_name = group_participant_cell_class_name[0]
    print(group_participant_cell_class_name)

    # Kirim pesan pada setiap anggota grup satu per satu
    group_participant_cells = driver.find_elements_by_class_name(
        group_participant_cell_class_name)
    print(group_participant_cells)
    for group_participant_cell in group_participant_cells:
        print(group_participant_cell)
        click(group_participant_cell, 'class', driver)
        if group_participant_cell.get_attribute(
                'class') != group_participant_cell_class_name:
            enter_keys(
                '//div[text()="' +
                language_hook_conf(user_input["user_language"], 4) + '"]',
                'xpath', user_input["message_to_send"], driver)
            click('//span[@title="' + user_input["group_name"] + '"]', 'xpath',
                  driver)
            click('//span[text()="' + user_input["group_name"] + '"]', 'xpath',
                  driver)

    print("Sampun")
    # driver.close()
