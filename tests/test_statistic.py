import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


async def test_get_statistic(async_client: AsyncClient) -> None:
    response = await async_client.get(
        '/statistic/?from=2024-03-07&to=2024-03-07&sort_by=date',
    )
    assert response.status_code == 200


async def test_get_statistic_without_params(async_client: AsyncClient) -> None:
    response = await async_client.get(
        '/statistic/?to=2024-03-07&sort_by=date',
    )
    assert response.status_code == 422
    response = await async_client.get(
        '/statistic/?from=2024-03-07&sort_by=date',
    )
    assert response.status_code == 422


async def test_create_statistic(async_client: AsyncClient) -> None:
    response = await async_client.post(
        '/statistic/',
        json={
            'date': '2024-03-07',
            'views': 10,
            'clicks': 100,
            'cost': 10,
        },
    )
    assert response.status_code == 201
    statistic = response.json()
    assert statistic == {
        'id': 1,
        'date': '2024-03-07',
        'views': 10,
        'clicks': 100,
        'cost': 10.0,
    }


async def test_get_one_statistic(async_client: AsyncClient) -> None:
    response = await async_client.post(
        '/statistic/',
        json={
            'date': '2024-03-07',
            'views': 10,
            'clicks': 100,
            'cost': 10,
        },
    )
    assert response.status_code == 201
    response = await async_client.get(
        '/statistic/?from=2024-03-07&to=2024-03-07&sort_by=date',
    )
    assert response.status_code == 200
    statistic = response.json()
    assert len(statistic) == 1


async def test_sort_statistic(async_client: AsyncClient) -> None:
    await async_client.post(
        '/statistic/',
        json={
            'date': '2024-03-08',
            'views': 10,
            'clicks': 10,
            'cost': 10,
        },
    )
    await async_client.post(
        '/statistic/',
        json={
            'date': '2024-03-09',
            'views': 5,
            'clicks': 5,
            'cost': 5,
        },
    )
    response = await async_client.get(
        '/statistic/?from=2024-03-08&to=2024-03-09&sort_by=date',
    )
    statistic = response.json()
    assert statistic[0]['date'] == '2024-03-08'
    response = await async_client.get(
        '/statistic/?from=2024-03-08&to=2024-03-09&sort_by=views',
    )
    statistic = response.json()
    assert statistic[0]['views'] == 5


async def test_delete_statistic(async_client: AsyncClient) -> None:
    await async_client.post(
        '/statistic/',
        json={
            'date': '2024-03-07',
            'views': 10,
            'clicks': 100,
            'cost': 10,
        },
    )
    response = await async_client.delete('/statistic/')
    assert response.status_code == 204
    response = await async_client.get(
        '/statistic/?from=2024-03-07&to=2024-03-07&sort_by=date'
    )
    statistic = response.json()
    assert len(statistic) == 0
