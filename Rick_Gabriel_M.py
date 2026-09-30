from __future__ import annotations

from datetime import date


class QuantidadeInvalidaError(Exception):
 "Indica uma quantidade invalida para movimentacao do estoque"


class MedicamentoVencidoError(Exception):
  "Indica tentativa de dispensar um lote vecido"


class Medicamento:

    def __init__(
        self,
        nome: str,
        lote: str,
        validade: date,
        quantidade: int,
        valor: float,
    ) -> None:
        self.nome = nome
        self.lote = lote
        self.validade = validade
        self.quantidade = quantidade
        self.valor = valor

@property
    def quantidade(self) -> int:
        return self._quantidade

 @quantidade.setter
    def quantidade(self, quantidade: int) -> None:
        if quantidade < 0:
            raise ValueError("A quantidade em estoque nao pode ser negativa")
        self._quantidade = quantidade

  @property
    def valor(self) -> float:
        return self._valor

@valor.setter
    def valor(self, valor: float) -> None:
        if not valor > 0:
            raise ValueError("O valor unitario deve ser maior que zero.")
        self._valor = valor

@classmethod
    def de_registro(cls, registro: str) -> Medicamento:
        campos = registro.split(";")
        if len(campos) != 5:
            raise ValueError(
                "O registro deve conter nome;lote;validade;quantidade;valor"
            )

        nome, lote, validade, quantidade, valor = campos
        return cls(
            nome=nome,
            lote=lote,
            validade=date.fromisoformat(validade),
            quantidade=int(quantidade),
            valor=float(valor),
        )

  @staticmethod
     def dias_para_vencer(validade: date) -> int:
        return (validade - date.today()).days

     def dispensar(self, quantidade: int) -> None:
        if quantidade <= 0 or quantidade > self.quantidade:
            raise QuantidadeInvalidaError(
                "A quantidade solicitada deve ser positiva e nao pode exceder o estoque"
            )
        if self.validade < date.today():
            raise MedicamentoVencidoError("Nao e possivel dispensar um lote vencido.")
        self.quantidade -= quantidade

     def repor(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade para reposicao deve ser positiva")
        self.quantidade += quantidade

     def __str__(self) -> str:
        return (
            f"{self.nome} ({self.lote}) - {self.quantidade} un. - "
            f"val. {self.validade.strftime('%d/%m/%Y')}"
        )

    def __repr__(self) -> str:
        return (
            f"Medicamento(nome={self.nome!r}, lote={self.lote!r}, "
            f"validade={self.validade!r}, quantidade={self.quantidade!r}, "
            f"valor={self.valor!r})"
        )

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Medicamento):
            return NotImplemented
        return self.nome == outro.nome and self.lote == outro.lote

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Medicamento):
            return NotImplemented
        return self.validade < outro.validade
