셀레니움에서 textarea에 multilined 문자열을 보낼때(send_keys) 라인별로 끊어서 보내면서,

각 라인의 끝은 `\n` 이나 `enter`가 아니라 `shift + enter`로 줄바꿈을 해야 할 때가 있다.

`element.send_keys(Keys.SHIFT, Keys.ENTER)`메서드를 통해 `shift + enter`기능을 쉽게 구현할 수 있었다.

`index.html`은 테스트 환경을 위한 페이지

