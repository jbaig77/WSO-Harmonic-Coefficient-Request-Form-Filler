from tkinter import*
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fields = 'Name', 'Address', 'Carrington Rotation', 'Center Longitude', 'Date', 'Order (<30)'

def getVal(entries, text):
    a = str(entries[text].get())
    return a

def func(entries):
    global name
    global address
    global cr
    global cl
    global date
    global order

    name = getVal(entries, 'Name')
    address = getVal(entries, 'Address')
    cr = getVal(entries, 'Carrington Rotation')
    cl = getVal(entries, 'Center Longitude')
    if (cl == "0"):
        cl = "180"
    date = getVal(entries, 'Date')
    order = getVal(entries, 'Order (<30)')

    root.quit()

def makeform(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row)
        ent.insert(0,"0")
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = Tk()
    root.title("WSO Harmonic Coefficent Request Form")
    ents = makeform(root, fields)
    b1 = Button(root, text="Submit", command = (lambda e=ents: func(e)))
    b1.pack(side=LEFT,padx=5,pady=5)
    root.mainloop()

    browser = webdriver.Firefox()
    browser.get('http://wso.stanford.edu/forms/prgs.html')

    browser.find_element_by_name('username').clear()
    name_field = browser.find_element_by_name('username')
    name_field.send_keys(name)

    browser.find_element_by_name('address').clear()
    address_field = browser.find_element_by_name('address')
    address_field.send_keys(address)

    browser.find_element_by_name('rotation').clear()
    rotation_field = browser.find_element_by_name('rotation')
    rotation_field.send_keys(cr)

    browser.find_element_by_name('order').clear()
    order_field = browser.find_element_by_name('order')
    order_field.send_keys(order)

    submit_button = browser.find_element_by_xpath('//input[@type="submit"]')
    submit_button.click()

    output = browser.find_element_by_css_selector('body')
    output.send_keys(Keys.CONTROL+'a')
    output.send_keys(Keys.CONTROL+'c')
    results = output.text

    text_file = open("Output.txt", "w")
    text_file.write(results)
    text_file.close()

    browser.close()

    with open("Output.txt", "r") as f:
        text = f.read()

    lines = text[text.find("h(uT)") + 5:].strip().split("\n")

    with open("new_output.csv", "w+") as f:
        for line in lines:
            l, m, g, h = line.split()
            f.write("{},{},{},{}\n".format(l, m, g, h))

