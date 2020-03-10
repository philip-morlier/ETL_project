class ListConverter():
    def __init__(self):
        pass
    
    def associate(self,list0,list1):
        dict_ = {}
        list_ = []
        for item in list0:
            for element in list1:
                if (str(element).lower()).find(item.lower())>0:
                    dict_.setdefault(item, []).append(element)
        return dict_

    def get_keys(self,a_list): 
        list_=[]
        dict_=a_list
        for key in dict_.keys(): 
            list_.append(key) 
          
        return list_