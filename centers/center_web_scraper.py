from urllib.request import urlopen


from centers.models import Center



def scrape_centers():
    Center.objects.all().delete()
    url = 'https://www.scratchbowling.com/bowling-centers?page='
    for x in range(0, 5):
        with urlopen(url + str(x)) as response:
            ##soup = BeautifulSoup(response, 'lxml')
            soup = None
            rows = soup.find_all(class_="views-row")
            for row in rows:
                name = row.find(class_="node__title")
                if name is not None:
                    name = name.find(class_="field--name-title")
                    if name is not None:
                        name = name.text

                address = row.find(class_="field--name-field-address")

                street = address.find(class_="address-line1")
                if street is not None: street = street.text

                city = address.find(class_="locality")
                if city is not None: city = city.text

                state = address.find(class_="administrative-area")
                if state is not None: state = state.text

                zip = address.find(class_="postal-code")
                if zip is not None: zip = zip.text

                phone = row.find(class_="field--name-field-phone-number")
                if phone is not None:
                    phone = phone.find("a")
                    if phone is not None:
                        phone = phone.text
                        phone = phone.replace('(','')
                        phone = phone.replace(')', '')
                        phone = phone.replace('-', '')
                        phone = phone.replace(' ', '')

                description = row.find(class_="field--type-text-long")
                if description is not None: description = description.text

                create_center(name, street, city, state, zip, phone, description)

def create_center(name, street, city, state, zip, phone, description):

    center = Center()
    center.center_name = name
    center.location_street = street
    center.location_city = city
    center.location_state = state
    center.location_zip = zip

    if phone is None:
        phone = 0
    center.phone_number = int(phone)
    center.center_description = str(description) + ' '
    center.save()
    print(Center.objects.count())