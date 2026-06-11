from utils.commands import SHOW_WIFI_PROFILES, SHOW_WIFI_PROFILE
from utils.execute import exec_command

profiles = exec_command(
    command_line=SHOW_WIFI_PROFILES,
    shell=True
)

names = [line.split(':')[1].strip() for line in profiles.split('\n') if 'All User Profile' in line]

for i, n in enumerate(names, 1):
    print(f'>>> [{i}] - {n}')

ch = int(input('\nChoose WIFI number: '))

wifi = names[ch - 1]

result = exec_command(
    command_line=SHOW_WIFI_PROFILE,
    arg=wifi,
    shell=True
)

password = [line.split(':')[1].strip() for line in result.split('\n') if 'Key Content' in line]

print("\n" + result)

if password:
    print(f'Key: {password[0]}')
