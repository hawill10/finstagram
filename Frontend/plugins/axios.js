export default function ({ $axios }) {
  $axios.onRequest(() => {
       config.headers.common['content-type'] = 'application/json'
  })
 }