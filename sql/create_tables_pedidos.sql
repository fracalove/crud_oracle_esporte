-- apaga os relacionamentos
ALTER TABLE AlunosEG DROP CONSTRAINT ALUNOS_PK;
ALTER TABLE ProfessoresEG DROP CONSTRAINT PROFESSORES_PK;
ALTER TABLE EsporteEG DROP CONSTRAINT ESPORTE_PK;

ALTER TABLE AlunosEG DROP CONSTRAINT ESPORTE_ALUNOS_FK;
ALTER TABLE ProfessoresEG DROP CONSTRAINT ESPORTE_PROFESSORES_FK;

-- apaga as tabelas
DROP TABLE EsporteEG;
DROP TABLE ProfessoresEG;
DROP TABLE AlunosEG;

-- apaga as sequences
DROP SEQUENCE ESPORTE_ID_ESPORTE_SEQ_1;
DROP SEQUENCE PROFESSOR_ID_PROFESSOR;
DROP SEQUENCE ALUNOS_MATRICULA_SEQ;


-- cria as tabelas
CREATE TABLE EsporteEG (
                id_esporte NUMBER NOT NULL,
                nome VARCHAR2(255) NOT NULL,
                coordenador VARCHAR2(255) NOT NULL,
                CONSTRAINT ESPORTE_PK PRIMARY KEY (id_esporte)
);

CREATE TABLE ProfessoresEG (
                id_professor NUMBER NOT NULL,
                nome VARCHAR2(255) NOT NULL,
                qtde_turmas NUMBER NOT NULL,
                id_esporte NUMBER NOT NULL,
                CONSTRAINT PROFESSORES_PK PRIMARY KEY (id_professor)
);

CREATE TABLE AlunosEG (
                matricula NUMBER NOT NULL,
                nome VARCHAR2(255) NOT NULL,
                cpf VARCHAR2(11) NOT NULL,
                id_esporte NUMBER NOT NULL,
                CONSTRAINT ALUNOS_PK PRIMARY KEY (matricula)
);

-- cria as sequences
CREATE SEQUENCE ESPORTE_ID_ESPORTE_SEQ_1;
CREATE SEQUENCE PROFESSOR_ID_PROFESSOR;
CREATE SEQUENCE ALUNOS_MATRICULA_SEQ;

-- cria os relacionamentos
ALTER TABLE AlunosEG ADD CONSTRAINT ESPORTE_ALUNOS_FK
FOREIGN KEY (id_esporte)
REFERENCES EsporteEG(id_esporte);

ALTER TABLE ProfessoresEG ADD CONSTRAINT ESPORTE_PROFESSORES_FK
FOREIGN KEY (id_esporte)
REFERENCES EsporteEG(id_esporte);





