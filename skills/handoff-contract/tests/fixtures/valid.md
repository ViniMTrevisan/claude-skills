# Payment Endpoint Handoff

## Goal
Implementar o endpoint de pagamento com resposta validada.

## Current state
DTO e teste existem; o teste falha com esperado 500 e recebido 400.

## Evidence
`python3 -m unittest tests.test_payment -v` falha na asserção de status em `tests/test_payment.py`.

## Decisions
Manter 400 para payload inválido; não alterar contrato sem revisar o teste.

## Next action
Execute `python3 -m unittest tests.test_payment -v` e revise `tests/test_payment.py` antes de editar o handler.

## Risks
Credenciais sandbox do gateway ainda não foram verificadas.

## Boundaries
Não fazer deploy em produção e não inserir segredo no repositório.

## Files
`tests/test_payment.py`, `src/payment.py`.
