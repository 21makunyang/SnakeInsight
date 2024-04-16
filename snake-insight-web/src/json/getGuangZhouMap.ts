export default $.ajax({
    url: 'https://geo.datav.aliyun.com/areas_v3/bound/440100_full.json',
    type: 'GET',
    success: function (data) {
        console.log(data);
    },
    error: function (err) {
        console.log(err);
    }
    });