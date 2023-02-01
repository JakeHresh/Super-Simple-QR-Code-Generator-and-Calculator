import re
import qrcode
from PIL import ImageDraw, ImageFont
import PySimpleGUI as sg

# QRCodeExample is a sample function that demonstrates the creation of a QR Code using the qrcode library.
def QRCodeExample():
    # Data to encode
    data = "15.00"

    # QR Code parameters in object
    qr = qrcode.QRCode(
        # version=1,
        # error_correction=qrcode.constants.ERROR_CORRECT_L,
        # box_size=10,
        border=6
    )

    # Encode data
    qr.add_data(data)
    qr.make(fit=True)

    # Save QR Code to image
    img = qr.make_image(fill_color="black", back_color="white")

    # Image drawing tool
    draw = ImageDraw.Draw(img)

    # Text font
    font = ImageFont.truetype("cambriab.ttf", 25)

    # Drawing text on image
    draw.text((110, 30), "CHAIR", font=font, fill=0)

    img.save("Code100.png")

def main():
    # Moved QR Code Example generation to designated method
    # QRCodeExample()
    window = sg.Window('Columns')
    col = [[]]

    calculator = [[]]

    item_index = 1
    items_count = 0

    calc_item_index = 1
    calc_items_count = 0

    layout = [
        [
            sg.Text('QR Code Pairs'), 
            sg.Column(col, scrollable=True, vertical_scroll_only=True, key='-COL LAB-', size=(850, 700)), 
            sg.Button('Add Item', enable_events=True, key='-ADD COL LAB-'), 
            sg.Button('Generate', enable_events=True, key='-GENERATE-'),
            sg.VerticalSeparator(), 
            sg.Text('Calculator'), 
            sg.Column(calculator, scrollable=True,  vertical_scroll_only=True, key='-COL CALC-', size=(500, 700)), 
            sg.Button('Add Price', enable_events=True, key='-ADD COL CALC-'),
            sg.Button('Total', enable_events=True, key='-CALC-'),
            sg.Text('', key="-PRICE DISPLAY-"), 
        ],
    ]
    
    calc_dex_list = []
    qr_dex_list = []
    regnumber = re.compile(r'\d+(?:,\d*)?')
    regfile = re.compile(r'[a-zA-Z0-9]')
    window = sg.Window('QR Code Reader and Generator', layout, size=(1870, 768), resizable=True)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
            break
        elif event.endswith('_LAB_REMOVE-'):
            item_column_key = event.replace('_LAB_REMOVE-', '')
            window[item_column_key].update(visible=False)
            window[item_column_key].Widget.master.pack_forget()
            window.visibility_changed()
            window['-COL LAB-'].contents_changed()
            values = window.read(timeout=100)
            qr_dex_list.remove(int(item_column_key.replace('-COL LAB-', '')))
            items_count -= 1
        elif event.endswith('_REMOVE-'):
            item_column_key = event.replace('_REMOVE-', '')
            print(item_column_key)
            window[item_column_key].update(visible=False)
            window[item_column_key].Widget.master.pack_forget()
            window.visibility_changed()
            window['-COL CALC-'].contents_changed()
            values = window.read(timeout=100)
            calc_dex_list.remove(int(item_column_key.replace('-COL CALC-', '')))
            calc_items_count -= 1
        elif event == '-ADD COL LAB-':
            new_col = [[sg.Text('Label: '), sg.Input('Label', key=f'-LAB VAL-{item_index}-'), sg.Text('Price: '), sg.Input('', key=f'-LAB PRICE-{item_index}-'), sg.Button('Remove', enable_events=True, key=f'-COL LAB-{item_index}_LAB_REMOVE-')]]
            window.extend_layout(window['-COL LAB-'], [[sg.Column(new_col, key=f'-COL LAB-{item_index}')]])
            window.visibility_changed()
            window['-COL LAB-'].contents_changed()
            values = window.read(timeout=100)
            qr_dex_list.append(item_index)
            item_index += 1
            items_count += 1
        elif event == '-ADD COL CALC-':
            new_col = [[sg.Text('Item: '), sg.Input('', key=f'-CALC VAL-{calc_item_index}-'), sg.Button('Remove', enable_events=True, key=f'-COL CALC-{calc_item_index}_REMOVE-')]]
            window.extend_layout(window['-COL CALC-'], [[sg.Column(new_col, key=f'-COL CALC-{calc_item_index}')]])
            window.visibility_changed()
            window['-COL CALC-'].contents_changed()
            values = window.read(timeout=100)
            calc_dex_list.append(calc_item_index)
            calc_item_index += 1
            calc_items_count += 1
        elif event == '-CALC-':
            current_calc_total = 0
            for calc_dex in calc_dex_list:
                if regnumber.match(window[f'-CALC VAL-{calc_dex}-'].get()):
                    current_calc_total += float(window[f'-CALC VAL-{calc_dex}-'].get())
            window['-PRICE DISPLAY-'].update(str(current_calc_total))
        elif event == '-GENERATE-':
            print('Hit Button')
            for code_dex in qr_dex_list:
                if regfile.match(window[f'-LAB VAL-{code_dex}-'].get()) and regnumber.match(window[f'-LAB PRICE-{code_dex}-'].get()):
                    print('Generating')
                    # Data to encode
                    data = window[f'-LAB PRICE-{code_dex}-'].get()
                    # QR Code parameters in object
                    qr = qrcode.QRCode(
                        border=6
                    )
                    # Encode data
                    qr.add_data(data)
                    qr.make(fit=True)
                    # Save QR Code to image
                    img = qr.make_image(fill_color="black", back_color="white")
                    # Image drawing tool
                    draw = ImageDraw.Draw(img)
                    # Text font
                    font = ImageFont.truetype("cambriab.ttf", 25)
                    # Drawing text on image
                    name = window[f'-LAB VAL-{code_dex}-'].get()
                    draw.text((110, 30), window[f'-LAB VAL-{code_dex}-'].get(), font=font, fill=0)
                    img.save(f'{name}.png')
            
        print(event, values)
        print(calc_dex_list)
        
    event, values = window.read()
    window.close()

if __name__ == "__main__":
    main()
