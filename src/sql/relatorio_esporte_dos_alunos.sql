-- junção de tabelas
SELECT a.matricula, a.nome, a.cpf, a.id_esporte, c.nome, c.coordenador
FROM AlunosEG a
INNER JOIN EsporteEG c
ON a.id_esporte = c.id_esporte
ORDER BY a.matricula
