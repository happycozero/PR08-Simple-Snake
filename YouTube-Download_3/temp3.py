from pytube import YouTube

link = input("Введите ссылку на видео: ")
video = YouTube(link)

print("\n")
print("Заголовок: " + video.title)
print("\n")
print("Изображение: " + video.thumbnail_url)
print("\n")
#stream = video.streams.filter(progressive=True)
stream = video.streams.get_by_itag(22)
stream.download()
print("Успешно!")