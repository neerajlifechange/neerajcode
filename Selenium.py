import subprocess

# Install wget
subprocess.run(['apt', 'install', 'wget', '-y'])

# Install webdriver_manager
subprocess.run(['pip', 'install', 'webdriver_manager'])

# Upgrade webdriver_manager
subprocess.run(['pip', 'install', '--upgrade', 'webdriver_manager'])

# Add Opera repository key
subprocess.run(['wget', '-qO-', 'https://deb.opera.com/archive.key', '|', 'apt-key', 'add', '-'])

# Add Opera repository
subprocess.run(['add-apt-repository', 'deb [arch=i386,amd64] https://deb.opera.com/opera-stable/ stable non-free'])

# Install Opera
subprocess.run(['apt', 'install', '-y', 'opera-stable'])

# Install selenium version 4.2.0
subprocess.run(['pip', 'install', 'selenium==4.2.0'])

# Install faker
subprocess.run(['pip', 'install', 'faker'])
