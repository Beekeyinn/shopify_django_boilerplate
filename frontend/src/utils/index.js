export const validateInputs = (datas) => {
  let obj = {};
  datas.forEach((data) => {
    Object.entries(data).map(([key, value], index) => {
      if (Array.isArray(value)) {
        if (value.length == 0 || value === null || value === undefined) {
          obj[key] = true;
        }
      } else if (typeof value === "number") {
        if (value < 0 || value === null || value === undefined) {
          obj[key] = true;
        }
      } else {
        if (value === "" || value === null || value === undefined) {
          obj[key] = true;
        }
      }
    });
  });
  console.log(obj);
  return obj;
};

export const getCsrfToken = () => {
  let name = "csrftoken";
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
