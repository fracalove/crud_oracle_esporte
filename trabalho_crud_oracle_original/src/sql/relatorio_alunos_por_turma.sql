select p.nome as professor, c.nome as nome_esporte, count(c.id_esporte) as qtde_alunos 
from alunosEG a
inner join professoresEG p
on a.id_esporte = p.id_esporte
inner join esporteEG c
on p.id_esporte = c.id_esporte
group by (p.nome, c.nome, c.id_esporte)
