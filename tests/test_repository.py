from database.repository import (
    create_contract,
    insert_document_chunk,
)


def test_insert_contract_and_chunk():
    contract_id = create_contract(
        "test_contract.docx"
    )

    chunk_id = insert_document_chunk(
        contract_id=contract_id,
        chunk_index=0,
        content="The supplier shall submit the report.",
        embedding=[0.1] * 384,
    )

    assert contract_id > 0
    assert chunk_id > 0
    