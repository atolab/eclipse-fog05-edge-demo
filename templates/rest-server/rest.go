package main

import (
	"context"
	"fmt"
	"log"
	"syscall"
	// "time"
	"bufio"
	"os"

	"github.com/containerd/containerd"
	"github.com/containerd/containerd/cio"
	"github.com/containerd/containerd/namespaces"
	"github.com/containerd/containerd/oci"
	"github.com/opencontainers/runtime-spec/specs-go"
)

func main() {
	if err := redisExample(); err != nil {
		log.Fatal(err)
	}
}

func redisExample() error {
	// create a new client connected to the default socket path for containerd
	client, err := containerd.New("/run/containerd/containerd.sock")
	if err != nil {
		return err
	}
	defer client.Close()

	// create a new context with an "fos" namespace
	ctx := namespaces.WithNamespace(context.Background(), "fos")

	imgName := fmt.Sprintf("docker.io/%s:latest", os.Args[1])
	// pull the redis image from DockerHub
	image, err := client.Pull(ctx, imgName, containerd.WithPullUnpack)
	if err != nil {
		return err
	}

	// getting a linux namespace to be connected to
	netNSName := fmt.Sprintf("/var/run/netns/%s", os.Args[2])
	netns := specs.LinuxNamespace{
		Type: specs.NetworkNamespace,
		Path: netNSName,
	}

	var opts_yaks []oci.SpecOpts
	var cOpts_yaks []containerd.NewContainerOpts
	var s_yaks specs.Spec
	var spec_yaks containerd.NewContainerOpts

	// setting opts
	cOpts_yaks = append(cOpts_yaks, containerd.WithImage(image))
	cOpts_yaks = append(cOpts_yaks, containerd.WithNewSnapshot(fmt.Sprintf("%s-snapshot", os.Args[3]), image))
	// cOpts = append(cOpts, containerd.WithRuntime("io.containerd.runc.v1", nil))
	opts_yaks = append(opts_yaks, oci.WithDefaultSpec(), oci.WithDefaultUnixDevices)
	opts_yaks = append(opts_yaks, oci.WithImageConfig(image))
	opts_yaks = append(opts_yaks, oci.WithLinuxNamespace(netns))

	spec_yaks = containerd.WithSpec(&s_yaks, opts_yaks...)
	cOpts_yaks = append(cOpts_yaks, spec_yaks)

	// create a container with yaks
	container_rest, err := client.NewContainer(
		ctx,
		os.Args[3],
		cOpts_yaks...,
	)
	if err != nil {
		return err
	}
	defer container_rest.Delete(ctx, containerd.WithSnapshotCleanup)

	// create a task from the container
	// task, err := container.NewTask(ctx, cio.NewCreator(cio.WithStdio))
	task_rest, err := container_rest.NewTask(ctx, cio.LogFile(fmt.Sprintf("/tmp/%s.log", os.Args[3])))
	if err != nil {
		return err
	}
	defer task_rest.Delete(ctx)

	// make sure we wait before calling start
	exitStatusC, err := task_rest.Wait(ctx)
	if err != nil {
		fmt.Println(err)
	}

	// call start on the task to execute the redis server
	if err := task_rest.Start(ctx); err != nil {
		return err
	}

	// wait user input to exit
	fmt.Print("Press 'Enter' to continue...")
	bufio.NewReader(os.Stdin).ReadBytes('\n')

	// kill the process and get the exit status
	if err := task_rest.Kill(ctx, syscall.SIGKILL); err != nil {
		return err
	}

	// wait for the process to fully exit and print out the exit status

	status := <-exitStatusC
	code, _, err := status.Result()
	if err != nil {
		return err
	}
	fmt.Printf("yaks-server exited with status: %d\n", code)
	//killing meao
	return nil
}
