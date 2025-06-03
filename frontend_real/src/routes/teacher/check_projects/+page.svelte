<script>
    import { onMount } from "svelte";
    import axios from "axios";

    let username = "";
    let projects = [];

    onMount(async () => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            const teacher_name = localStorage.getItem("teacher_name") || "teacher1";
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/v1/projects/teacher/${teacher_name}`);
                projects = response.data;
            } catch (error) {
                console.error("Error fetching projects:", error);
            }
        }
    });
</script>



<div class="border-1 border-gray-300 rounded-box p-4">
    <div class="bg-purple-100 rounded-sm h-10 flex items-center pl-2">查看学生项目</div>
    <div class="rounded-box border border-base-content/5 bg-base-100 mt-4">
  <table class="table">
    <!-- head -->
    <thead>
      <tr>
        <th></th>
        <th>题目</th>
        <th>描述</th>
        <th>状态</th>
        <th>开始日期</th>
        <th>更新日期</th>
      </tr>
    </thead>
    <tbody>
      {#each projects as project, index}
      <tr>
        <th>{index + 1}</th>
        <td>{project.title}</td>
        <td>{project.description}</td>
        <td>{project.status}</td>
        <td>{new Date(project.start_date).toLocaleDateString()}</td>
        <td>{new Date(project.update_time).toLocaleString()}</td>
      </tr>
      {/each}
    </tbody>
  </table>
</div>
</div>




