
<script>
    import axios from "axios";
    import '$lib/style.css';
    import { onMount } from 'svelte';

    let selections = $state([]);
    let filterTerm = $state('');
    let currentPage = $state(1);
    let total = $state(0);

    // 弹窗相关
    let showEditModal = $state(false);
    // 当前要编辑的选题信息
    let editingSelection = $state({});

    // 打开弹窗并复制选题信息
    function openEditModal(selection) {
        editingSelection = { ...selection };
        showEditModal = true;
    }

    // 关闭弹窗
    function closeEditModal() {
        showEditModal = false;
        editingSelection = {};
    }

    // 确认编辑
    async function confirmEdit() {
        try {
            await axios.put(`http://127.0.0.1:8000/api/v1/selections/admin/${editingSelection.id}`, {
                ...editingSelection
            });
            closeEditModal();
            fetchData();
        } catch (error) {
            console.log(error);
        }
    }

    // 获取数据
    async function fetchData() {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/selections/selections/paginate?page=${currentPage}`);
            selections = response.data.selections;
            total = response.data.total;
        } catch (error) {
            console.log(error);
        }
    }

    // 筛选
    function filteredSelections() {
        if (!filterTerm) return selections;
        return selections.filter(item =>
            item.username?.toLowerCase().includes(filterTerm.toLowerCase()) ||
            item.title?.toLowerCase().includes(filterTerm.toLowerCase())
        );
    }

    // 分页控制
    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            fetchData();
        }
    }
    function nextPage() {
        currentPage++;
        fetchData();
    }

    // 删除
    async function deleteSelection(id) {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/v1/selections/admin/${id}`);
            fetchData();
        } catch (error) {
            console.log(error);
        }
    }

    onMount(() => {
        fetchData();
    });
</script>

<main class="p-4">
    <h1 class="text-2xl font-bold mb-4">查看所有选题</h1>
    <!-- 搜索框 -->
    <div class="mb-4">
        <input
          class="input input-bordered w-full"
          type="text"
          placeholder="搜索用户名或题目"
          bind:value={filterTerm}
        />
    </div>

    <div class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>用户名</th>
                    <th>专业</th>
                    <th>题目</th>
                    <th>描述</th>
                    <th>状态</th>
                    <th>创建时间</th>
                    <th>更新时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {#each filteredSelections() as selection}
                    <tr>
                        <td>{selection.id}</td>
                        <td>{selection.username}</td>
                        <td>{selection.major}</td>
                        <td>{selection.title}</td>
                        <td>{selection.description}</td>
                        <td>{selection.status}</td>
                        <td>{new Date(selection.created_time).toLocaleString()}</td>
                        <td>{new Date(selection.update_time).toLocaleString()}</td>
                        <td>
                            <button class="btn btn-primary btn-xs mr-2" on:click={() => openEditModal(selection)}>编辑</button>
                            <button class="btn btn-error btn-xs" on:click={() => deleteSelection(selection.id)}>删除</button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <!-- 分页按钮 -->
    <div class="mt-4 flex gap-4">
        <button class="btn" on:click={prevPage}>上一页</button>
        <button class="btn" on:click={nextPage}>下一页</button>
    </div>

    <!-- 弹窗 -->
    {#if showEditModal}
    <div class="fixed inset-0 flex items-center justify-center bg-opacity-40">
        <div class="bg-white p-8 rounded-lg w-96 border-1 shadow-2xs">
            <h2 class="text-xl font-bold mb-4">编辑选题</h2>
            <div class="form-control mb-4">
                <label class="label">题目</label>
                <input
                  bind:value={editingSelection.title}
                  type="text"
                  class="input input-bordered"
                />
            </div>
            <div class="form-control mb-4">
                <label class="label">描述</label>
                <textarea
                  bind:value={editingSelection.description}
                  rows="3"
                  class="textarea textarea-bordered"
                ></textarea>
            </div>
            <div class="form-control mb-4">
                <label class="label">状态</label>
                <input
                  bind:value={editingSelection.status}
                  type="text"
                  class="input input-bordered"
                />
            </div>
            <div class="flex justify-end">
                <button class="btn btn-secondary mr-2" on:click={closeEditModal}>取消</button>
                <button class="btn btn-primary" on:click={confirmEdit}>保存</button>
            </div>
        </div>
    </div>
    {/if}
</main>