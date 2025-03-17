<script>
    let { children } = $props();
    import { setContext } from 'svelte';
  import { onMount } from 'svelte';
  import '$lib/style.css';

  let username = '';
  let student_id = 0;

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      student_id = localStorage.getItem('student_id')
      console.log(username);
      console.log(student_id);
    }
  });
</script>

{@render children()}