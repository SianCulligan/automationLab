# Once emails and phone numbers are found they should be stored in two separate documents.


import re

# file paths
file_path = 'automationlab/potential-contacts.txt'
existing_customers = 'automationlab/existing-contacts.txt'
clean_emails = 'automationlab/emails.txt'
clean_phone_numbers = 'automationlab/phone_numbers.txt'
# contents = ''

#get file contents
def open_contents(file):
    # f = open('potential-contacts.txt', 'r')
    # print(f.read)
    with open(file, 'r') as reader:
        read_lines = reader.read()
        # for line in reader.readlines():
    # contents += read_lines
    # print('read lines', read_lines)
    return read_lines

# open_contents()


#pull phone numbers
# The information should be sorted in ascending order.
def get_phone_numbers(file):
    opened_file = open_contents(file)
    regex_code = r'((\(\d{3}\)|\d{3})?[\s-]?(\d{3})[\s-]?(\d{4})(x\d+)?)'
    check_doc = re.findall(regex_code, opened_file)
    
    final_list = number_formating_helper(check_doc)
    final_list.sort()
    # print(final_list)
    return final_list

# get_phone_numbers()

# Pull emails
def get_emails(file):
    list_of_emails = []
    opened_file = open_contents(file)
    regex_code = '\S+@\S+'
    email_lst = re.findall(regex_code, opened_file)

    #eliminate dupes in return list
    for entry in email_lst:
        print('TRAVERSING ENTRIES', entry)
        if not entry in list_of_emails:
            list_of_emails.append(entry)

    list_of_emails.sort()
    print('EMAILS', list_of_emails)
    return list_of_emails


def write_emails(existing_file, new_file):
    opened_emails = get_emails(new_file)
    get_existing_emails = get_emails(existing_file)

    # remove dupes comparing 'old' file to 'new' before writing to new file 
    for entry in get_existing_emails: 
        print('TRAVERSING ENTRIES', entry)
        if entry in opened_emails:
            opened_emails.remove(entry)

    # write the info to a new email.txt file
    with open(clean_emails, 'w') as file:
        write_it_to_file = file.write('\n'.join(opened_emails))


def write_phone_numbers(existing_file, new_file):
    opened_numbers = get_phone_numbers(new_file)
    get_existing_numbers = get_phone_numbers(existing_file)

    # remove dupes comparing 'old' file to 'new' before writing to new file 
    for entry in get_existing_numbers: 
        print('TRAVERSING ENTRIES', entry)
        if entry in opened_numbers:
            opened_numbers.remove(entry)

    # write the info to a new email.txt file
    with open(clean_phone_numbers, 'w') as file:
        file.write('\n'.join(opened_numbers))


# Helper functions
def number_formating_helper(checked_doc):
    list_of_nums = []

    for entry in checked_doc:
        # print('IN CHECK DOC LOOP', entry)
        add_to_num = ''
        #add 206 if area code doesn't exist
        if not len(entry[1]):
            add_to_num += '206'
            # print('ADD TO', add_to_num)
        #extract area codes, no parens
        elif len(entry[1]) == 5:
            add_to_num += entry[1][1:4]
            # print('ADD TO', add_to_num)
        #happy path
        else: 
            add_to_num += entry[1]
            # print('ADD TO', add_to_num)       

        #concatenatie and format (XXX-XXX-XXXX)
        format_num = f'{add_to_num}-{entry[2]}-{entry[3]}'

        #check list, don't add dupes
        if not format_num in list_of_nums:
            list_of_nums.append(format_num)
    
    return list_of_nums
# get_emails()

if __name__ == "__main__":
    write_phone_numbers(existing_customers, file_path)
    write_emails(existing_customers, file_path)