class DivideList(object):
    """
    Split list into n groups.
    Effectively distribute the elements of list to each group
    ex) group_n =3, list= [1,2,3,4,5]
    => [1,2], [3,4], [5]
    """
    def __init__(self):
        pass
        
        
    def divide_chunks(self, table_list:list, group_n:int):  
        """
        :param table_list: list to be splitted
        :param group_n: number of group
        """
        self.table_list= table_list
        self.group_n= group_n
        
        if len(self.table_list) <= self.group_n:
            self.group_n = len(self.table_list)
        quotient, remainder= divmod( len(self.table_list), self.group_n) 

        for i in range(0, len(self.table_list), quotient):  

            yield self.table_list[i:i + quotient] 
    
    
    def convert_chunks(self, divided_chunk):
        
        x = list(divided_chunk) 
        quotient, remainder= divmod( len(self.table_list), self.group_n) 
        #print('quotient :',quotient,"remainder :", remainder)
        if remainder==0:
            return x
        else:
            if quotient >= remainder:
                for i in range(remainder):
                    x[-(i+2)].extend([x[self.group_n][i]])
                return x[:-1]
            else :
                 for i in range(remainder):
                     x[-(i+self.ceiling(remainder/quotient)+1)].extend([x[self.group_n+int(i/quotient)][i%quotient]])
                 return x[:-self.ceiling(remainder/quotient)]
    
    @staticmethod
    def ceiling(n):
        if float(n).is_integer():
            return int(n)
        else:
            return int(n)+1
if __nam__=='__main__':

    A= DivideList()
    group_n=6
    res= A.convert_chunks(A.divide_chunks(my_list, group_n))
