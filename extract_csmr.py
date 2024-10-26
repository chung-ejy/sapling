from csmarapi.CsmarService import CsmarService
from csmarapi.ReportUtil import ReportUtil
from dotenv import load_dotenv
load_dotenv()
import os

csmar = CsmarService()
csmar.login(os.getenv("CSMRACCOUNT"),os.getenv("CSMRPW"),"1")
tables = csmar.getListTables('Stock Market Trading')
ReportUtil(tables)