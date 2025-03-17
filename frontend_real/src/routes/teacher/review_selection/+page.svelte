<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import '$lib/style.css';

    let username = '';
    let selections = [];
    let error = '';
    let loading = false;

    // 响应式声明，始终根据 selection.id 从小到大排序
    $: sortedSelections = selections.slice().sort((a, b) => a.id - b.id);

    async function handleSubmit() {
        loading = true;
        error = '';
        try {
            const res = await axios.get(`http://127.0.0.1:8000/api/v1/selections/teacher/${username}`);
            selections = res.data;
            console.log(selections);
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
            
        }
    }

    async function updateSelectionStatus(studentId, newStatus) {
        try {
            await axios.put(`http://127.0.0.1:8000/api/v1/selections/teacher/${studentId}`, { status: newStatus });
            // 修改成功后重新刷新数据列表
            await handleSubmit();
        } catch (err) {
            error = err.message;
        }
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
            username = localStorage.getItem('username') || '用户';
            console.log(username);
        }
        // 页面加载时自动获取数据
        handleSubmit();
    });
</script>

<div class="border-1 border-gray-300 rounded-box p-4">
    <div class="bg-purple-100 rounded-sm h-10 flex items-center pl-2">审核学生申报题目</div>
    
    {#if loading}
        <div class="mt-4 text-gray-500">加载中...</div>
    {:else if error}
        <div class="mt-4 text-red-500">{error}</div>
    {:else}
        <div class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100 mt-4">
            <table class="table">
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>姓名</th>
                        <th>专业</th>
                        <th>论文标题</th>
                        <th>论文描述</th>
                        <th>学生id</th>
                        <th>创建时间</th>
                        <th>更新时间</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {#each sortedSelections as selection}
                        <tr>
                            <th>{selection.id}</th>
                            <td>{selection.username}</td>
                            <td>{selection.major}</td>
                            <td>{selection.title}</td>
                            <td>{selection.description}</td>
                            <td>{selection.student_id}</td>
                            <td>{new Date(selection.created_time).toLocaleString()}</td>
                            <td>{new Date(selection.update_time).toLocaleString()}</td>
                            <td>{selection.status}</td>
                            <td>
                                <button class="btn btn-soft btn-primary btn-sm mr-2" on:click={() => updateSelectionStatus(selection.student_id, '通过')} disabled={selection.status === '通过'}>
                                    通过
                                </button>
                                <button class="btn btn-soft btn-primary btn-sm" on:click={() => updateSelectionStatus(selection.student_id, '拒绝')}>
                                    拒绝
                                </button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>