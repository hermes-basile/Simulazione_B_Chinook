from database.DB_connect import DBConnect
from model.genere import Genere


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from genre g
                """

        cursor.execute(query)

        for row in cursor:
            results.append( Genere(**row)

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(paese):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.GenreId 
                from customer c , invoice i ,invoiceline i2 , track t  
                where c.CustomerId = i.CustomerId and i.InvoiceId = i2.InvoiceId  and t.TrackId = i2.TrackId  
                and c.Country = %s
                order by t.GenreId asc 
                    """

        cursor.execute(query, (paese,))

        for row in cursor:
            results.append(
                row["GenreId"]

                           )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def fillListaCopieVendute(nodo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select sum(Quantity) as Quantity
                    from invoiceline i , track t
                    where i.TrackId = t.TrackId 
                    and t.GenreId = %s
                                   """

        cursor.execute(query,(nodo.GenreId,))

        for row in cursor:
            nodo.numero_copie =  row["Quantity"]



        cursor.close()
        conn.close()

    @staticmethod
    def fillListaClienti(nodo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct i.CustomerId  
                from invoice i , invoiceline i2 , track t 
                where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId 
                and t.GenreId = %s
                order by i.CustomerId asc 
                                   """

        cursor.execute(query, (nodo.GenreId,))

        for row in cursor:
            results.append(
                row["CustomerId"]
            )

        cursor.close()
        conn.close()
        nodo.lista_id_clienti = results

    @staticmethod
    def fillListaClientiPaese(nodo, paese):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct i.CustomerId  
                    from invoice i , invoiceline i2 , track t , customer c 
                    where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId and c.CustomerId = i.CustomerId 
                    and t.GenreId = %s
                    and c.Country = %s
                    order by i.CustomerId asc 
                                      """

        cursor.execute(query, (nodo.GenreId, paese))

        for row in cursor:
            results.append(
                row["CustomerId"]
            )

        cursor.close()
        conn.close()
        nodo.lista_id_clienti_paese = results

    @staticmethod
    def lista_paesi():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Country 
                    from customer c 
                    order by c.Country asc 
                        """

        cursor.execute(query, )

        for row in cursor:
            results.append(
                row["Country"]

            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def fillListaCopieVendutePaese(nodo, paese):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select sum(Quantity) as Quantity
                    from invoiceline i , track t, invoice i2 , customer c 
                    where i.TrackId = t.TrackId  and i2.InvoiceId  = i.InvoiceId and i2.CustomerId = c.CustomerId 
                    and t.GenreId = %s
                    and c.Country = %s
                                      """

        cursor.execute(query, (nodo.GenreId, paese))

        for row in cursor:
            nodo.numero_copie_paese = row["Quantity"]

        cursor.close()
        conn.close()


