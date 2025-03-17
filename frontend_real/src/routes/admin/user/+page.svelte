<script>
  import { tick } from 'svelte';
  import axios from 'axios';
  import '$lib/style.css';

  let editUserModal;
  let users = $state([]);
  let loading = $state(true);
  let error = $state(null);
  let editingUser = $state(null);
  let currentPage = $state(1);
  let totalPages = $state(1);
  const itemsPerPage = 10;

  const fetchUsers = async (page = 1) => {
    loading = true;
    error = null;
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/users/users/paginate?page=${page}`, {
        headers: { accept: 'application/json' },
      });
      users = response.data.users;
      totalPages = Math.ceil(response.data.total / itemsPerPage);
      currentPage = page;
    } catch (err) {
      error = err;
    } finally {
      loading = false;
    }
  };

  const editUser = async (user) => {
    editingUser = { ...user };
    await tick();
    editUserModal?.showModal();
  };

  const saveEdit = async () => {
    if (!editingUser.username || !editingUser.role) {
      alert('请填写用户名和角色');
      return;
    }
    try {
      const response = await axios.put(`http://127.0.0.1:8000/api/v1/users/${editingUser.id}`, editingUser, {
        headers: { accept: 'application/json', 'Content-Type': 'application/json' },
      });
      const index = users.findIndex((user) => user.id === editingUser.id);
      if (index !== -1) {
        users[index] = response.data;
      }
      editUserModal.close();
      editingUser = null;
    } catch (err) {
      error = err;
    }
  };

  const cancelEdit = () => {
    editUserModal.close();
    editingUser = null;
  };

  const deleteUser = async (userId) => {
    if (confirm('确定要删除此用户吗？')) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/v1/users/${userId}`, {
          headers: { accept: 'application/json' },
        });
        users = users.filter((user) => user.id !== userId);
      } catch (err) {
        error = err;
      }
    }
  };

  const changePage = (page) => {
    if (page > 0 && page <= totalPages) {
      fetchUsers(page);
    }
  };

  $effect(() => {
    fetchUsers();
  });
</script>

<style>
  html {
    overflow-y: overlay;
  }
</style>

<main>
  {#if loading}
    <p>加载中...</p>
  {:else if error}
    <p>加载失败：{error.message}</p>
  {:else}
    <div class="overflow-x-auto m-20 border-1">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th></th>
            <th>用户名</th>
            <th>角色</th>
            <th>学生 ID</th>
            <th>教师 ID</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {#each users as user}
            <tr>
              <th>{user.id}</th>
              <td>{user.username}</td>
              <td>{user.role}</td>
              <td>{user.student_id}</td>
              <td>{user.teacher_id}</td>
              <td>
                <button class="btn btn-sm btn-soft btn-primary" on:click={() => editUser(user)}>编辑</button>
                <button class="btn btn-sm btn-danger" on:click={() => deleteUser(user.id)}>删除</button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if editingUser}
      <dialog bind:this={editUserModal} id="editUserModal" class="modal">
        <div class="modal-box">
          <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
          <h3 class="text-lg font-bold">编辑用户</h3>
          <form on:submit|preventDefault={saveEdit}>
            <div class="form-control">
              <label class="label">
                <span class="label-text">用户名</span>
              </label>
              <input type="text" class="input input-bordered" bind:value={editingUser.username} required />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">角色</span>
              </label>
              <input type="text" class="input input-bordered" bind:value={editingUser.role} required />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">学生 ID</span>
              </label>
              <input type="number" class="input input-bordered" bind:value={editingUser.student_id} />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">教师 ID</span>
              </label>
              <input type="number" class="input input-bordered" bind:value={editingUser.teacher_id} />
            </div>
            <div class="modal-action">
              <button class="btn btn-soft btn-primary" type="submit">保存</button>
              <button class="btn btn-ghost" type="button" on:click={cancelEdit}>取消</button>
            </div>
          </form>
        </div>
      </dialog>
    {/if}

    <div class="flex justify-center mt-4">
      <div class="join">
        <button class="join-item btn btn-square w-18" on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>上一页</button>
        {#each Array(totalPages).fill(0) as _, i}
          <button class="join-item btn btn-square {currentPage === i + 1 ? 'btn-active' : ''}" on:click={() => changePage(i + 1)}>{i + 1}</button>
        {/each}
        <button class="join-item btn btn-square w-18" on:click={() => changePage(currentPage + 1)} disabled={currentPage === totalPages}>下一页</button>
      </div>
    </div>
  {/if}
</main>
