import pickle

insta_username = 'doronshai_creative'
insta_password = 'Ilmbfvm20189'
users_i_follow = ['natalia_tellez','lajosa','verge','thrillist','olyria_roy','edenfines','avital_akko','coral.sharon','sapir_elgrabli','noharbatit','yarden3ardity','roni_brachel1','moran.titanchi','max164','diana_tre','sapir_perez','moran_dvoskin','moran_aroch','sapirmichaeli_','shir_tikozky','sky_buskila','adi_edri9','shirrrrrraaa_elbaz','madlen_tequila','danigozlan5397','yael_ovadia','djtristanofficial','12sivan12','koral_shmuel11','dana_vyun','itssany']

file_Name = "variables.pickle"
# open the file for writing
fileObject = open(file_Name,'wb') 

# this writes the object a to the
# file named 'testfile'
pickle.dump([insta_username, insta_password, users_i_follow],fileObject)   

# here we close the fileObject
fileObject.close()
