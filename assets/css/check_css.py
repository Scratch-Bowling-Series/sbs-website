import os
import tinycss


def read_css(file_name):
    try:
        f = open(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name, "r")
        return f.read()
    except FileNotFoundError:
        return None

def main():

    desktop = 'desktop-large.css'
    mobile = 'phone-large.css'
    desktop = read_css(desktop)
    mobile = read_css(mobile)
    if desktop != None and mobile != None:
        parser = tinycss.make_parser('page3')
        desktop = parser.parse_stylesheet(desktop)
        mobile = parser.parse_stylesheet(mobile)
        missing = compare_lists(desktop.rules, mobile.rules, 'phone-large.css');
        compare_lists(mobile.rules, desktop.rules, 'desktop-large.css');
        for miss in missing:
            print(str(miss))
    else:
        print('not found at: ' + os.path.dirname(os.path.realpath(__file__)) + '/' + 'desktop-large.css')

def compare_lists(one, two, file_name):
    dont_exist_list = []
    for rule in one:
        matched = False
        for other in two:
            if rule.selector.as_css() == other.selector.as_css():
                matched = True
                break
        if matched == False:
            dont_exist_list.append(str(rule.selector.as_css()))

    print('Done! ' + str(len(dont_exist_list)) + " rules dont exist in '" + file_name + "'.")
    return dont_exist_list


if __name__ == "__main__":
    main()


