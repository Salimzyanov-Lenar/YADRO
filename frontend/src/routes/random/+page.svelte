<script lang="ts">
    import { onMount } from "svelte";

    let user: {
        id: number;
        gender: string;
        first_name: string;
        second_name: string;
        phone_number: string;
        email: string;
        residing_place: string;
        photo_url: string;
    } | null = $state(null); 

    let error: string | null = $state(null);

     async function loadUser() {
        try {
            // users = await fetchUsers(limit, skip);
            const response = await fetch(`/api/users/v1/random`);
            if (!response.ok) {
                throw new Error("Ошибка при загрузке пользователей");
            }

            user = await response.json();
        
        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = String(err);
            }
        }
    }

    onMount(loadUser);
</script>


<h1 class="title">Профиль пользователя</h1>

{#if error}
  <p class="error">{error}</p>
{:else if !user}
  <p class="loading">Загрузка пользователя...</p>
{:else}
  <div class="user-card">
    <img src={user.photo_url} alt="Фото пользователя" class="avatar" />
    <h2>{user.first_name} {user.second_name}</h2>
    <p><strong>Пол:</strong> {user.gender}</p>
    <p><strong>Телефон:</strong> {user.phone_number}</p>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Место проживания:</strong> {user.residing_place}</p>
  </div>
{/if}

<a href={`/`} class="back-link"><button>Вернуться к списку пользователей</button></a>

<style>
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-family: 'Inter', sans-serif;
        margin-bottom: 2rem;
    }

    .error {
        color: red;
        text-align: center;
        font-weight: bold;
    }

    .loading {
        text-align: center;
        font-style: italic;
    }

    .user-card {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 12px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-family: 'Inter', sans-serif;
    }

    .user-card h2 {
        margin-bottom: 1rem;
        font-size: 1.75rem;
    }

    .user-card p {
        margin: 0.5rem 0;
        font-size: 1rem;
        color: #333;
    }

    .avatar {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
        margin-bottom: 1rem;
        border: 2px solid #ddd;
    }

    .back-link {
        display: block;
        text-align: center;
        margin-top: 2rem;
        text-decoration: none;
        font-size: 1.1rem;
        color: #0d6efd;
        transition: color 0.2s ease;
        font-family: 'Inter', sans-serif;
    }

    .back-link:hover {
        color: #084298;
    }

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

</style>