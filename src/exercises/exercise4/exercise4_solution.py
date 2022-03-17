'''
Give an range of ip address- start-ip and end-ip, check if the given-ip fall in between
start-ip and end-ip.

start-ip    10.30.20.50
end-ip      10.31.20.50

'''


def is_within_range(start_ip, end_ip, ip_value):
    # int_start_ip = int(start_ip.replace('.', ''))
    # int_end_ip = int(end_ip.replace('.', ''))
    # int_ip_value = int(ip_value.replace('.', ''))

    int_start_ip = int(''.join(start_ip.split('.')))
    int_end_ip = int(''.join(end_ip.split('.')))
    int_ip_value = int(''.join(ip_value.split('.')))

    if int_start_ip <= int_ip_value <= int_end_ip:
        return  True
    return False


def is_within_range_alt(start_ip, end_ip, ip_value):
    int_start_ip =  weighted_ip_value(start_ip)
    int_end_ip   =  weighted_ip_value(end_ip)
    int_ip_value =  weighted_ip_value(ip_value)

    if int_start_ip <= int_ip_value <= int_end_ip:
        return True
    return False

def weighted_ip_value(str_ip):
    ip_arr = str_ip.split('.')
    return  (int(ip_arr[0])<<24) + (int(ip_arr[1])<<16) + (int(ip_arr[2])<<8) + int(ip_arr[3])


if __name__ == '__main__':
    start_ip = '10.20.30.50'
    end_ip   = '10.20.31.10'
    curr_ip  = '10.20.30.51'
    print(f'is_within_range     -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range(start_ip,end_ip,curr_ip)}')
    print(f'is_within_range_alt -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range_alt(start_ip,end_ip,curr_ip)}')

    curr_ip = '10.20.30.49'
    print(f'is_within_range     -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range(start_ip,end_ip,curr_ip)}')
    print(f'is_within_range_alt -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range_alt(start_ip,end_ip,curr_ip)}')

    curr_ip = '10.20.30.58'
    print(f'is_within_range     -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range(start_ip,end_ip,curr_ip)}')
    print(f'is_within_range_alt -->{start_ip}, {end_ip}, {curr_ip} : {is_within_range_alt(start_ip,end_ip,curr_ip)}')