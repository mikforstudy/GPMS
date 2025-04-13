
<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let username = '';
  let selections = {};
  let loading = false;
  let error = '';


  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      console.log(username);
      
    }
    getData();
  });

  async function getData() {
    loading = true;
    error = '';
    try {
      // 1. 获取当前学生项目
      const res = await axios.get(`http://127.0.0.1:8000/api/v1/selections/student/${username}`);
      selections = res.data;

      // 2. 根据 teacher_id 调用接口并补充教师用户名
      for (const sel of selections) {
        if (sel.teacher_id) {
          const teacherRes = await axios.get(`http://127.0.0.1:8000/api/v1/users/get_teacher_username/${sel.teacher_id}`);
          sel.teacher_username = teacherRes.data.username;
        }
      }
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="border-1 border-gray-300 rounded-box p-4">
  <div class="bg-purple-100 rounded-sm h-10 flex items-center pl-2">查看个人项目</div>
  
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
            <th>专业</th>
            <th>题目标题</th>
            <th>题目描述</th>
            <th>状态</th>
            <th>指导教师</th>
          </tr>
        </thead>
        <tbody>
          {#each selections as selection}
            <tr>
              <td>{selection.id}</td>
              <td>{selection.major}</td>
              <td>{selection.title}</td>
              <td class="break-words">{selection.description}</td>
              <td>{selection.status}</td>
              <td>{selection.teacher_username || '无'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>


<style>
  .break-words {
    word-break: break-word;
    white-space: pre-wrap;
  }
</style>