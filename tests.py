from cutlists import Cutlist
c=Cutlist('Marvel_s_Agents_of_S_H_I_E_L_D___Wake_Up_17.01.24_22-00_uswabc_60_TVOON_DE.mpg.HQ.avi')
#c=Cutlist('433135674',mode='ofsb') #filesize
c.search(mode='name')
c.sort_cutlists()
c.download(toprated=True)