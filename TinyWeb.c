#include "csapp.h"

void doit(int fd);
void read_requesthdrs(int fd);
int parse_uri(char *uri, char *filename, char *cgiargs);
void serve_static(int fd, char * filename, int filesize);
void get_filetype(char *filename, char *filetype);
void serve_dynamic(int fd, char *filename, char *cgiargs);
void clienterror(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg);

int main(int argc, char **argv){
	int listenfd, connfd, port, clientlen, optval = 1;
	struct sockaddr_in clientaddr;
	struct sockaddr_in serveraddr;

	if (argc != 2){
		fprintf(stderr, "usage: %s <port>\n", argv[0]);
		exit(1);
	}

	port = atoi(argv[1]);

	if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
		printf("socket error\n");
		return -1;
	}

	if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval, sizeof(int)) < 0){
		printf("Address already in use\n");
		return -1;
	}

	bzero((char*)&serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons((unsigned short)port);
	
	if (bind(listenfd, (SA *)&serveraddr, sizeof(serveraddr)) < 0){
		printf("bind error\n");
		return -1;
	}

	if (listen(listenfd, LISTENQ) < 0){
		printf("listen error\n");
 		return -1;
	}

	while(1){
		clientlen = sizeof(clientaddr);
		printf("Wait for client\n");
		connfd = accept(listenfd, (SA *)&clientaddr, &clientlen);
		printf("Connect successful!\n");
		doit(connfd);
		close(connfd);		
	}
	return 0;
}

int readline(int fd, void *usrbuf, int maxlen){
	int n, rc;
	char c, *bufp = usrbuf;

	for (n = 1; n < maxlen; n++){
		if ((rc = read(fd, &c, 1)) == 1){
			*bufp++ = c;
			if (c == '\n'){
				break;
			}
		}else if (rc == 0){
			if (n == 1)
				return 0;
			else
				break;
		}else
			return -1;
	}	
	*bufp = 0;
	return n;
}

void doit(int fd){
	int is_static;
	struct stat sbuf;
	char buf[MAXLINE], method[MAXLINE], uri[MAXLINE], version[MAXLINE];
	char filename[MAXLINE], cgiargs[MAXLINE];

	readline(fd, buf, MAXLINE);
	sscanf(buf, "%s %s %s", method, uri, version);
	if (strcasecmp(method, "GET")){
		clienterror(fd, method, "501", "NOT Implemented", "Tiny does not implement this method");
		return;
	}
	read_requesthdrs(fd);

	is_static = parse_uri(uri, filename, cgiargs);

	if (stat(filename, &sbuf) < 0){
		clienterror(fd, filename, "404", "Not found", "Tiny could't find this file");
		return;
	}

	if (is_static){
		if (!(S_ISREG(sbuf.st_mode)) || !(S_IRUSR & sbuf.st_mode)){
			clienterror(fd, filename, "403", "Forbiidden", "Tiny couldn't read the file");
			return;
		}
		serve_static(fd, filename, sbuf.st_size);	
	}else{
		if (!(S_ISREG(sbuf.st_mode)) || !(S_IXUSR & sbuf.st_mode)){
			clienterror(fd, filename, "403", "Forbidden", "Tiny counldn't run the CGI program");
			return;
		}
		serve_dynamic(fd, filename, cgiargs);
	}
}

void clienterror(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg){
	char buf[MAXLINE], body[MAXLINE];

	sprintf(body, "<html><title> Tiny Error </title>");
	sprintf(body, "%s<body bgcolor = ""ffffff"">\r\n", body);
	sprintf(body, "%s%s: %s\r\n", body, errnum, shortmsg);
	sprintf(body, "%s<p>%s: %s\r\n", body, longmsg, cause);
	sprintf(body, "%s<hr><em> The Tiny Web server</em>\r\n", body);

	sprintf(buf, "HTTP/1.0 %s %s\r\n", errnum, shortmsg);
	write(fd, buf, strlen(buf));
	sprintf(buf, "Content-type: text/html\r\n");
	write(fd, buf, strlen(buf));
	sprintf(buf, "Content-type-length: %d\r\n\r\n", (int)strlen(body));
	write(fd, buf, strlen(buf));
	write(fd, body, strlen(body));
}

void read_requesthdrs(int fd){
	char buf[MAXLINE];

	readline(fd, buf, MAXLINE);
	while(strcmp(buf, "\r\n")){
		readline(fd, buf, MAXLINE);
		printf("%s", buf);
	}
}

void serve_static(int fd, char *filename, int filesize){
	int srcfd;
	char *srcp, filetype[MAXLINE], buf[MAXLINE];

	get_filetype(filename, filetype);
	sprintf(buf, "HTTP/1.0 200 OK\r\n");
	sprintf(buf, "%sServer: Tiny Web Server\r\n", buf);
	sprintf(buf, "%sContent-legth: %d\r\n", buf, filesize);
	sprintf(buf, "%sContent-type: %s\r\n\r\n", buf, filetype);
	write(fd, buf, strlen(buf));
	
	srcfd = open(filename, O_RDONLY, 0);
	srcp = mmap(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0);
	close(srcfd);
	write(fd, srcp, filesize);
	munmap(srcp, filesize);
}

int parse_uri(char *uri, char *filename, char *cgiargs){
    char *ptr;

    if(!strstr(uri, "cgi-bin")){
        strcpy(cgiargs, "");
        strcpy(filename, ".");
        strcat(filename, uri);
        if(uri[strlen(uri)-1] == '/'){
            strcat(filename, "login.html");
	}     
	return 1;
    }else{
        ptr = index(uri, '?');
        if(ptr){
            strcpy(cgiargs, ptr+1);
            *ptr = '\0';
        }else{
            strcpy(cgiargs, "");
	}        
	strcpy(filename, ".");
        strcat(filename, uri);
        return 0;
    }
}

void get_filetype(char *filename, char *filetype){
	if (strstr(filename, ".html"))
		strcpy(filetype, "text/html");
	else if (strstr(filename, ".gif"))
		strcpy(filetype, "image/gif");
	else if (strstr(filename, ".jpg"))
		strcpy(filetype, "image/jpeg");
	else
		strcpy(filetype, "text/plain");
}

void serve_dynamic(int fd, char *filename, char *cgiargs){
	char buf[MAXLINE], *emptylist[] = { NULL};

	sprintf(buf, "HTTP/1.0 200 OK\r\n");
	printf("Hello\n");
	printf("%s\n", buf);
	write(fd, buf, strlen(buf));
	sprintf(buf, "Server: Tiny Web Server\r\n");
	write(fd, buf, strlen(buf));

	if (fork() == 0){
		setenv("QUERY_STRING", cgiargs, 1);
		dup2(fd, STDOUT_FILENO);
		execve(filename, emptylist, environ);
	}
	wait(NULL);
}




























