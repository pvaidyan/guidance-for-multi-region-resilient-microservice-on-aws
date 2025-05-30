FROM amazoncorretto:17-al2-full as build-env

ARG JAR_PATH

VOLUME /tmp
WORKDIR /

COPY .mvn .mvn
COPY mvnw .
COPY pom.xml .

RUN ./mvnw dependency:go-offline -B -q

COPY ./src ./src

RUN ./mvnw -DskipTests package -q && mv ./target/orders-0.0.1-SNAPSHOT.jar /app.jar

# Package Stage
FROM amazoncorretto:17-al2-full

ARG aws_opentelemetry_agent_version=1.24.0

RUN yum install -q -y \
    shadow-utils wget && \
    yum clean all

ENV APPUSER=appuser
ENV APPUID=1000
ENV APPGID=1000

RUN useradd \
    --home "/app" \
    --create-home \
    --user-group \
    --uid "$APPUID" \
    "$APPUSER"

RUN wget https://github.com/aws-observability/aws-otel-java-instrumentation/releases/download/v${aws_opentelemetry_agent_version}/aws-opentelemetry-agent.jar -O /opt/aws-opentelemetry-agent.jar && \
    wget https://raw.githubusercontent.com/aws-observability/aws-otel-java-instrumentation/v${aws_opentelemetry_agent_version}/licenses/licenses.md -O aws-opentelemetry-agent-licenses.md
#ENV JAVA_TOOL_OPTIONS=-javaagent:/opt/aws-opentelemetry-agent.jar
#ENV OTEL_JAVAAGENT_ENABLED=false

WORKDIR /app
USER appuser

COPY ./ATTRIBUTION.md ./LICENSES.md
COPY --chown=appuser:appuser --from=build-env /app.jar .

EXPOSE 8080
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1
ARG JAVA_OPTS

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]