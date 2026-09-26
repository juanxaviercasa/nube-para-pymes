for mod in ['deep_translator', 'googletrans', 'translate', 'requests', 'urllib3']:
    try:
        __import__(mod)
        print(f'{mod}: available')
    except ImportError:
        print(f'{mod}: NOT available')
