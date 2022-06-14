import rpa as r
import csv
import boto3
import time
from selenium import webdriver
from PIL import Image
from pathlib import Path

name_brand = 'gucci_d#'
INPUT_LINKS = 'https://www.yoox.com/us/women/clothing/shoponline/gucci_d#/d=42&dept=clothingwomen&gender=D'

header = 'Handle,Title,Body (HTML),Vendor,Standardized Product Type,Custom Product Type,Tags,Published,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Variant Barcode,Original Image Src,Image Src,Image Position,Image Alt Text,Gift Card,SEO Title,SEO Description,Google Shopping / Google Product Category,Google Shopping / Gender,Google Shopping / Age Group,Google Shopping / MPN,Google Shopping / AdWords Grouping,Google Shopping / AdWords Labels,Google Shopping / Condition,Google Shopping / Custom Product,Google Shopping / Custom Label 0,Google Shopping / Custom Label 1,Google Shopping / Custom Label 2,Google Shopping / Custom Label 3,Google Shopping / Custom Label 4,Variant Image,Variant Weight Unit,Variant Tax Code,Cost per item,Status'
header_list = header.split(',')

print(len(header_list))


with open(f'out {name_brand}.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(header_list)


def get_item_links():
    item_links = []
    checker_list = []
    for page in range(1, 10000):
        if checker_list == []:
            pass
        elif len(checker_list) == 1 and page - 1 == checker_list[0]:
            break
        elif len(checker_list) > 1 and page - 1 == checker_list[-1]:
            break
        checker_list.append(page)
        print(page, '==========')
        r.url(
            f'{INPUT_LINKS}&page={page}')

        time.sleep(15)
        for it in range(1, 130):
            try:
                print(r.read(
                    f'//html/body/div[1]/section[2]/main/div/div/div/div[9]/div[2]/div/div/div[{it}]/div/div[2]/a/@href'))
                item_links.append('https://www.yoox.com' + r.read(
                    f'//html/body/div[1]/section[2]/main/div/div/div/div[9]/div[2]/div/div/div[{it}]/div/div[2]/a/@href'))
                checker_list.append('https://www.yoox.com')
            except:
                break

    print(item_links)
    return item_links


def main():
    item_links_list = get_item_links()
    #item_links_list = ['https://www.yoox.com/us/15098353UF/item#dept=clothingwomen&sts=SearchResult&cod10=15098353UF&sizeId=-1']
    for link in item_links_list:
        #try:
            r.url(link)
            time.sleep(10)
            brand = r.read('//html/body/div[1]/div[2]/div/main/div[2]/div/h1/a')
            print(brand)

            category = r.read('//html/body/div[1]/div[2]/div/main/div[2]/div/h2/a')
            print(category)

            description = r.read('//html/body/div[1]/div[2]/div/main/div[6]/div/div[2]/div[1]/div[2]/span')
            print(description)

            try:
                #/html/body/div[1]/div[2]/div/main/div[2]/div/div/div[1]/div[2]
                price = r.read('//html/body/div[1]/div[2]/div/main/div[2]/div/div[1]/div[2]/div/span')
                print(price)
            except:
                price = r.read('//html/body/div[1]/div[2]/div/main/div[2]/div/div/div[1]/div[2]/span')
                print(price)

            tag2 = r.read('/html/body/div[1]/div[2]/div/main/div[5]/span[2]/span[1]/a')
            print(tag2)

            tag3 = r.read('/html/body/div[1]/div[2]/div/main/div[5]/span[3]/span[1]/a')
            print(tag3)

            tag4 = r.read('/html/body/div[1]/div[2]/div/main/div[5]/span[4]/span[1]/a')
            print(tag4)

            num_first = 1

            for color_range in range(1, 100):
                try:
                    r.click(f'/html/body/div[1]/div[2]/div/main/div[3]/div/div[1]/div[2]/div[{color_range}]')
                except:
                    break
            #/html/body/div[1]/div[2]/div/main/div[3]/div/div[1]/div[2]/div[2]

                color_name = r.read(f'/html/body/div[1]/div[2]/div/main/div[3]/div/div[1]/div[2]/div[{color_range}]/div[1]/@title')

                time.sleep(2)

                size_list = []
                for size in range(1, 100):
                    try:
                        size_list.append(r.read(f'//html/body/div[1]/div[2]/div/main/div[3]/div/div[2]/div/div/div/div[{size}]/div[1]/div[1]/span'))
                    except:
                        break

                print(size_list)

                image_list = []
                for img in range(1, 100):
                    try:
                        image_list.append(str(r.read(f'//html/body/div[1]/div[2]/div/main/div[1]/div/div/div[2]/div[{img}]/img/@src')).replace('_10_', '_14_'))
                    except:
                        break


                print(image_list)

                check_list = [len(image_list), len(size_list)]

                max_value_list = max(check_list)

                print(max_value_list)

                for max_digit in range(3):
                    if len(image_list) == max_value_list:
                        pass
                    elif len(image_list) < max_value_list:
                        add_count = max_value_list - len(image_list)
                        for im_list in range(add_count):
                            image_list.append('')

                    if len(size_list) == max_value_list:
                        pass
                    elif len(size_list) < max_value_list:
                        add_count = max_value_list - len(size_list)
                        for sz_list in range(add_count):
                            size_list.append('')



                for im, im_size_col in enumerate(zip(image_list, size_list)):
                    print(im, im_size_col)
                    print(type(im))
                    if num_first == 1:
                        [f.unlink() for f in Path("imgs3").glob("*") if f.is_file()]
                        #https://www.yoox.com/images/items/16/16067833JG_14_r.jpg
                        driver = webdriver.Chrome(executable_path='driver/chromedriver')
                        driver.get(im_size_col[0])
                        time.sleep(3)
                        driver.save_screenshot(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}.png")
                        driver.close()

                        img = Image.open(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}.png")

                        box = (755, 0, 1645, 1134)
                        img2 = img.crop(box)

                        img2.save(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}1.png")

                        s3 = boto3.client('s3', aws_access_key_id='AKIA442H4KFW42KYDFGP',
                                          aws_secret_access_key='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')

                        s3.upload_file(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}1.png", 'yo-img', f"{im_size_col[0].split('/')[-1].split('.')[0]}.png",
                                       ExtraArgs={'ContentType': "image/png", 'ACL': "public-read"})

                        for ex_code in s3.exceptions._code_to_exception:
                            print(ex_code)

                        with open(f'out {name_brand}.csv', 'a') as f:
                            # create the csv writer
                            writer = csv.writer(f)

                            # write a row to the csv file
                            writer.writerow(
                                [f'{brand}', f'{brand}', f'{description}', f'{brand}', '', f'{category}', f'{tag2}, {tag3}, {tag4}', 'TRUE', 'Size', f'{im_size_col[1]}',
                                 'Color', f'{color_name}', '', '', '', '', '', '', '', f'{price}', '', '', '', '',
                                 f'{im_size_col[0]}', f"https://yo-img.s3.amazonaws.com/{im_size_col[0].split('/')[-1].split('.')[0]}.png", f'{num_first}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                 ''])
                    else:

                        [f.unlink() for f in Path("imgs3").glob("*") if f.is_file()]
                        # https://www.yoox.com/images/items/16/16067833JG_14_r.jpg
                        if im_size_col[0] != '':
                            driver = webdriver.Chrome(executable_path='driver/chromedriver')
                            driver.get(im_size_col[0])
                            time.sleep(3)
                            driver.save_screenshot(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}.png")
                            driver.close()

                            img = Image.open(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}.png")

                            box = (755, 0, 1645, 1134)
                            img2 = img.crop(box)

                            img2.save(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}1.png")

                            s3 = boto3.client('s3', aws_access_key_id='AKIA442H4KFW42KYDFGP',
                                              aws_secret_access_key='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')

                            s3.upload_file(f"imgs3/{im_size_col[0].split('/')[-1].split('.')[0]}1.png", 'yo-img',
                                           f"{im_size_col[0].split('/')[-1].split('.')[0]}.png",
                                           ExtraArgs={'ContentType': "image/png", 'ACL': "public-read"})

                            for ex_code in s3.exceptions._code_to_exception:
                                print(ex_code)

                            with open(f'out {name_brand}.csv', 'a') as f:
                                # create the csv writer
                                writer = csv.writer(f)

                                # write a row to the csv file
                                writer.writerow(
                                    ['', '', f'', f'', '', f'', '', '', '', f'{im_size_col[1]}',
                                     '', f'{color_name}', '', '', '', '', '', '', '', f'{price}', '', '', '', '',
                                     f'{im_size_col[0]}', f"https://yo-img.s3.amazonaws.com/{im_size_col[0].split('/')[-1].split('.')[0]}.png", f'{num_first}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                     ''])
                        else:
                            with open(f'out {name_brand}.csv', 'a') as f:
                                # create the csv writer
                                writer = csv.writer(f)

                                # write a row to the csv file
                                writer.writerow(
                                    ['', '', f'', f'', '', f'', '', '', '', f'{im_size_col[1]}',
                                     '', f'{color_name}', '', '', '', '', '', '', '', f'{price}', '', '', '', '',
                                     f'{im_size_col[0]}',
                                     f"",
                                     f'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                     ''])

                    num_first += 1
        #except:
            #continue


if __name__ == '__main__':
    r.init()
    r.error(True)
    main()
    r.close()