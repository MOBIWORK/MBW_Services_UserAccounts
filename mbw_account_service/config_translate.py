import mbw_account_service
import i18n
import os

base_file_path = os.path.dirname(mbw_account_service.__file__)
i18n.load_path.append(base_file_path + '/translations')
