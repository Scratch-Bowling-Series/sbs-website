


def update_center_with_soup(center, soup):
    name = soup.find(class_='title')
    if name:
        name = name.find('span')
        if name:
            name = name.text
    name = name or ''

    address = soup.find(class_='address')
    if address:
        street = address.find(class_='address-line1')
        if street:
            street = street.text
        city = address.find(class_='locality')
        if city:
            city = city.text
        state = address.find(class_='administrative-area')
        if state:
            state = state.text
        zip = address.find(class_='postal-code')
        if zip:
            zip = zip.text
            if zip:
                zip = int(zip)

    phone = soup.find(class_="field--name-field-phone-number")
    if phone:
        phone = phone.find("a")
        if phone:
            phone = phone.text
            phone = phone.replace('(', '')
            phone = phone.replace(')', '')
            phone = phone.replace('-', '')
            phone = phone.replace(' ', '')
    phone = phone or 0

    description = soup.find(class_="field--name-field-website")
    if description:
        description = description.find("a")
        if description:
            description = description.text
    description = description or ''


    center.center_name = name
    center.location_street = street
    center.location_city = city
    center.location_state = state
    center.location_zip = zip
    center.phone_number = int(phone)
    center.center_description = str(description)

