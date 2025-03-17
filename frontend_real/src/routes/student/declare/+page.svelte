<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import "$lib/style.css";

    let username = $state("");
    let student_id = $state(0);
    let teacher_id = $state(1);
    let major = $state("");
    let title = $state("");
    let description = $state("");
    let feedbackMessage = $state("");
    let feedbackType = $state("");

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            student_id = localStorage.getItem("student_id");
            console.log(username);
        }
    });

    async function submitForm(event) {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/selections/student/', {
                student_id,
                teacher_id,
                username,
                major,
                title,
                description
            });
            feedbackMessage = '提交成功！';
            feedbackType = 'success';
            console.log('Response:', response.data);
        } catch (error) {
            feedbackMessage = '提交失败，检查教师ID是否正确，请勿重复提交。';
            feedbackType = 'error';
            console.error('Error:', error);
        }
    }
</script>

<div class="max-w-lg mx-auto p-8 space-y-4 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-semibold text-center">申报题目</h2>
    
    <form onsubmit={submitForm} class="space-y-4">
        <div class="form-control">
            <label class="label" for="student_id">
                <span class="label-text">学生ID:</span>
            </label>
            <input type="number" id="student_id" bind:value={student_id} class="input input-bordered w-full" required disabled />
        </div>

        <div class="form-control">
            <label class="label" for="teacher_id">
                <span class="label-text">教师ID:</span>
            </label>
            <input type="number" id="teacher_id" bind:value={teacher_id} class="input input-bordered w-full" required />
        </div>

        <div class="form-control">
            <label class="label " for="username">
                <span class="label-text">用户名:</span>
            </label>
            <input type="text" id="username" bind:value={username} class="input input-bordered w-full" required disabled/>
        </div>

        <div class="form-control">
            <label class="label" for="major">
                <span class="label-text">专业:</span>
            </label>
            <input type="text" id="major" bind:value={major} class="input input-bordered w-full" required />
        </div>

        <div class="form-control">
            <label class="label" for="title">
                <span class="label-text">题目:</span>
            </label>
            <input type="text" id="title" bind:value={title} class="input input-bordered w-full" required />
        </div>

        <div class="form-control">
            <label class="label" for="description">
                <span class="label-text">描述:</span>
            </label>
            <textarea id="description" bind:value={description} class="textarea textarea-bordered w-full" rows="4" required></textarea>
        </div>

        <div class="form-control mt-4">
            <button type="submit" class="btn btn-soft btn-primary w-full">提交</button>
        </div>
    </form>

    {#if feedbackMessage}
        <div role="alert" class="alert {feedbackType === 'success' ? 'alert-success' : 'alert-error'} mt-4">
            <span>{feedbackMessage}</span>
        </div>
    {/if}

    <div role="alert" class="alert alert-info mt-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="h-6 w-6 shrink-0 stroke-current">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>请检查确认后提交</span>
    </div>
</div>