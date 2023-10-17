from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros
        self.qry_total_alunos = config.QUERY_COUNT.format(tabela="alunosEG")
        self.qry_total_esportes = config.QUERY_COUNT.format(tabela="esporteEG")
        self.qry_total_professores = config.QUERY_COUNT.format(tabela="professoresEG")


        # Informações do Criador
        self.created_by = "Daniel Vitor, Flavio Moreira, Gabriel Louzada e Gabriel Vianna"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"


    def get_total_alunos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()

        # retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_alunos).values[0]

    def get_total_esportes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()

        # retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_esportes).values[0]

    def get_total_professores(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()

        # retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_professores).values[0]


    def get_updated_screen(self):
        return f"""
        ########################################################
        #            SISTEMA DE ESCOLA DE ESPORTES                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - ALUNOS:         {str(self.get_total_alunos()).rjust(5)}
        #      2 - ESPORTES:         {str(self.get_total_esportes()).rjust(5)}
        #      3 - PROFESSORES:    {str(self.get_total_professores()).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """
