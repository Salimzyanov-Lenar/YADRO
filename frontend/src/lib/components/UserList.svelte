<script lang="ts">
    import { onMount } from "svelte";

    let users = $state<Array<{
        id: number,
        gender: string,
        first_name: string, 
        second_name: string, 
        phone_number: string,
        email: string, 
        residing_place: string, 
        photo_url: string
    }>>([]);

    let limit = $state(100);
    let skip = $state(0);

    let hasNext = $state(false);
    let totalAmount = $state(0);

    
    let error: string | null = $state(null);

     async function loadUsers() {
        try {
            // users = await fetchUsers(limit, skip);
            const response = await fetch(`/api/users/v1?skip=${skip}&limit=${limit}`);
            if (!response.ok) {
                throw new Error("Ошибка при загрузке пользователей");
            }

            const data = await response.json();

            users = data.users;
            hasNext = data.has_next;
            totalAmount = data.total_amount; 

        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = String(err);
            }
        }
    }

    onMount(loadUsers);

    function nextPage() {
        if (skip + limit < totalAmount) {
        skip += limit;
            loadUsers();
        }  
    }

    function prevPage() {
        skip = Math.max(0, skip - limit);
        loadUsers();
    }

    function changeLimit(newLimit: number) {
        limit = newLimit;
        skip = 0;
        loadUsers();
    }
</script>




<h1 style="text-align: center">Отображать по {limit} пользователей</h1>
<div style="margin: 20px; max-width: fit-content; margin-inline: auto;">
    <button onclick={() => changeLimit(10)} >10</button>
    <button onclick={() => changeLimit(30)} >30</button>
    <button onclick={() => changeLimit(50)} >50</button>
    <button onclick={() => changeLimit(100)} >100</button>
</div>

<div style="margin: 20px; max-width: fit-content; margin-inline: auto;">
    <a href={`/random/`}><button>Случайный пользователь</button></a>
</div>

<h1 style="text-align: center">Пользователи</h1>

<div style="margin: 20px; max-width: fit-content; margin-inline: auto;">
    <button onclick={prevPage} disabled={skip === 0}>Назад</button>
    <button onclick={nextPage} disabled={skip + limit >= totalAmount} >Вперёд</button>
</div>

{#if error}
    <p style="color: red;">Ошибка получения данных</p>
{:else if users.length === 0}
    <p>Загрузка пользователей...</p>
{:else}
    <div class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>Фото</th>
                    <th>Пол</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>Телефон</th>
                    <th>Email</th>
                    <th>Город</th>
                    <th>Профиль</th>
                </tr>
            </thead>
            <tbody>
                {#each users as user}
                    <tr>
                        <td><img src="{user.photo_url}" alt="photo" class="user-photo" /></td>
                        <td>{user.gender}</td>
                        <td>{user.first_name}</td>
                        <td>{user.second_name}</td>
                        <td>{user.phone_number}</td>
                        <td>{user.email}</td>
                        <td>{user.residing_place}</td>
                        <td><a href={`/` + user.id}><button>Страница</button></a></td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

<div style="margin: 20px; max-width: fit-content; margin-inline: auto;">
    <button onclick={prevPage} disabled={skip === 0}>Назад</button>
    <button onclick={nextPage}>Вперёд</button>
</div>


<style>

    h1 {
        font-family: 'Inter', sans-serif;
    }

    /* BUTTON STYLES */
    button {
        align-items: center;
        appearance: none;
        background-color: #FCFCFD;
        border-radius: 4px;
        border-width: 0;
        box-shadow: rgba(45, 35, 66, 0.4) 0 2px 4px,rgba(45, 35, 66, 0.3) 0 7px 13px -3px,#D6D6E7 0 -3px 0 inset;
        box-sizing: border-box;
        color: #36395A;
        cursor: pointer;
        display: inline-flex;
        font-family: "JetBrains Mono",monospace;
        height: 48px;
        justify-content: center;
        line-height: 1;
        list-style: none;
        overflow: hidden;
        padding-left: 50px;
        padding-right: 50px;
        position: relative;
        text-align: left;
        text-decoration: none;
        transition: box-shadow .15s,transform .15s;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        white-space: nowrap;
        will-change: box-shadow,transform;
        font-size: 16px;
    }

    button:focus {
        box-shadow: #D6D6E7 0 0 0 1.5px inset, rgba(45, 35, 66, 0.4) 0 2px 4px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
    }

    button:hover {
        box-shadow: rgba(45, 35, 66, 0.4) 0 4px 8px, rgba(45, 35, 66, 0.3) 0 7px 13px -3px, #D6D6E7 0 -3px 0 inset;
        transform: translateY(-2px);
    }

    button:active {
        box-shadow: #D6D6E7 0 3px 7px inset;
        transform: translateY(2px);
    }

    button:disabled {
        background-color: #e0e0e0;
        color: #a0a0a0;
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
    }

    /* TABLE STYLES */
    .table-wrapper {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 1rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 0 12px rgba(0, 0, 0, 0.08);
        overflow: hidden;
    }

    thead {
        background-color: #f8f9fa;
    }

    th, td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
    }

    th {
        font-weight: 600;
        color: #343a40;
        background-color: #e9ecef;
    }

    tr:hover {
        background-color: #f1f3f5;
        transition: background-color 0.2s ease-in-out;
    }

    .user-photo {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* LINKS STYLES */
    a {
        color: #0d6efd;
        text-decoration: none;
        font-weight: 500;
    }

    a:hover {
        text-decoration: underline;
    }

</style>

