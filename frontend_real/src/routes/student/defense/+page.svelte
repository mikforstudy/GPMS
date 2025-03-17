<script>
    import { onMount } from "svelte";
    import axios from "axios";

    let username = "";
    let student_id = 0;
    let defenses = [];

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            student_id = localStorage.getItem("student_id");
            fetchDefenseData();
        }
    });

    async function fetchDefenseData() {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/defense/student/${student_id}`);
            defenses = response.data;
        } catch (error) {
            console.error("Error fetching defense data:", error);
        }
    }
</script>

<h1 class="text-2xl font-bold mb-4">答辩信息</h1>
<div class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-md">
  <table class="min-w-full divide-y divide-gray-200">
    <!-- head -->
    <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学生姓名</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">教师姓名</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">项目标题</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩教室</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩组</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩阶段</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩日期</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each defenses as defense, index}
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{index + 1}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.student_name}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.teacher_name}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.project_title}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_class}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_group}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_phase}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_date}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.status}</td>
      </tr>
      {/each}
    </tbody>
  </table>
</div>